r"""
Generate some samples by templates
       implement follow
       Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference ACL2019
       In order to generate some sample whose premise is the sequence of the hypothesis but the semantic are different.
==========================================================
"""

from ..transformation import Transformation
from ....common.utils.overlap_templates import *
from ....input_layer.component.sample import SMSample

__all__ = ['Overlap']


def no_the(sentence):
    return sentence.replace("the ", "")


def repeaters(sentence):
    condensed = no_the(sentence)
    words = []

    for word in condensed.split():
        if word in lemma:
            words.append(lemma[word])
        else:
            words.append(word)

    if len(list(set(words))) == len(words):
        return False
    else:
        return True


class Overlap(Transformation):
    r"""
    Generate some samples by templates which implement follow
        Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural
        Language Inference ACL2019

       In order to generate some sample whose premise is the sequence of the
       hypothesis but the semantic are different.

    Exmaple::

       {
            sentence1: I hope Tom can go to school.
            sentence2: Tom go to school.
            y: 0
       }

    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'Overlap'

    def transform(self, sample, n=1, **kwargs):
        r"""
        Transform data sample to a list of Sample.

        :param ~SMSample sample: Data sample for augmentation
        :param int n: Default is 1. MAX number of unique augmented output
        :param **kwargs:
        :return: Augmented data

        """
        transform_results = self._transform(n, **kwargs)

        if transform_results:
            return transform_results
        else:
            return []

    def _transform(self, n=1, **kwargs):
        r"""
        Transform text string, this kind of transformation can only produce
        one sample.

        :param ~NLISample sample: input data, a NLISample contains
            'sentence1' field, 'sentence2' field and 'y' field
        :param int n: number of generated samples, this transformation can
            only generate one sample
        :return list trans_samples: transformed sample list that only
            contain one sample

        """
        example_counter = 0
        trans_list = []

        for template_tuple in template_list:
            label = template_tuple[2]
            if label == 'entailment':
                label = '1'
            else:
                label = '0'
            template = template_tuple[3]

            example_dict = {}
            # TODO, random select template
            count_examples = 0

            while count_examples < n:
                example = template_filler(template)

                example_sents = tuple(example[:2])

                if example_sents not in example_dict and not repeaters(
                        example[0]):
                    example_dict[example_sents] = 1
                    trans_sample = {
                        'sentence1': example[0],
                        'sentence2': example[1],
                        'y': label
                    }
                    trans_list.append(SMSample(trans_sample))
                    count_examples += 1
                    example_counter += 1

        return trans_list
