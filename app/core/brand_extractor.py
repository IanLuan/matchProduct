import codecs
import os
import numpy as np
import keras
from keras_self_attention import Attention
from keras_contrib.layers import CRF
from keras_wc_embd import get_dicts_generator, get_batch_input


class BrandExtractor:
    def __init__(self):
        self.tags = {
            'O': 0,
            'B': 1,
            'I': 2,
            'E': 3,
        }
        self.load_embeddings()
        self.load_model()

    
    def load_embeddings(self):
        self.word_dict = {
            '': 0,
            '<UNK>': 1,
        }
        self.word_embd_weights = [
            [0.0] * 100,
            np.random.random((100,)).tolist(),
        ]

        with codecs.open(os.path.join(os.path.dirname(__file__), 'utils', 'glove_s100.txt'), 'r', 'utf8') as reader:
            for line_num, line in enumerate(reader):
                if (line_num + 1) % 1000 == 0:
                    print('Load embedding... %d' % (line_num + 1), end='\r', flush=True)
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                word = parts[0].lower()
                if word not in self.word_dict:
                    self.word_dict[word] = len(self.word_dict)
                    self.word_embd_weights.append(parts[1:])

        self.word_embd_weights = np.asarray(self.word_embd_weights, dtype=object)
        #print('Dict size: %d  Shape of weights: %s' % (len(self.word_dict), str(self.word_embd_weights.shape)))
        print("Finished embedding")

    
    def load_model(self):
        print("Started building model")
        input_layer = keras.layers.Input(shape=(None,))

        embd_layer = keras.layers.Embedding(input_dim=len(self.word_dict),
                                        output_dim=100,
                                        mask_zero=True,
                                        trainable=True,
                                        name='Embedding')(input_layer)

        lstm_layer = keras.layers.Bidirectional(keras.layers.LSTM(units=100,
                                                              recurrent_dropout=0.4,
                                                              return_sequences=True),
                                            name='Bi-LSTM')(embd_layer)

        attention_layer = Attention(attention_activation='sigmoid',
                                attention_width=9,
                                return_attention=False,
                                name='Attention')(lstm_layer)
    
        crf = CRF(units=len(self.tags), sparse_target=True, name='CRF')

        outputs = [crf(attention_layer)]
        loss = {'CRF': crf.loss_function}

        self.model = keras.models.Model(inputs=input_layer, outputs=outputs)
        self.model.compile(
            optimizer=keras.optimizers.Adam(lr=1e-3),
            loss=loss,
            metrics={'CRF': crf.accuracy},
        )

        print("Finished building model")

        print("Started loading weights")
        self.model.load_weights(os.path.join(os.path.dirname(__file__), 'utils', 'model'), by_name=True)
        self.model._make_predict_function()
        print("Finished loading model")

    
    def extract(self, product):
        product = product.lower()
        product = product.split()
        sample_input = []
        
        for word in product:
            if word in self.word_dict:
                sample_input.append(self.word_dict[word])
            else:
                sample_input.append(self.word_dict['<UNK>'])
        
        while len(sample_input) < 4:
            sample_input.append(0)

        sample_input = np.asarray([sample_input])
        print("Sample input: ", sample_input)

        predict = self.model.predict_on_batch(sample_input)
        predict = np.argmax(predict, axis=2).tolist()

        predict = [w for w, tag in zip(product, predict[0]) if tag in [self.tags["B"],self.tags["I"],self.tags["E"]]]
        return " ".join(predict)
