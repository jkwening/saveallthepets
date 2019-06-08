import unittest
from math import ceil
from breed_id.data_loader import DogBreedDataLoader

# NOTE: must map to local directory of images
IMG_DIR = '/media/wdblack-1/saveallthepets/dog-breed-dataset/kaggle/train'
# Kaggle dataset can be found:
# https://www.kaggle.com/c/dog-breed-identification/data


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._loader = DogBreedDataLoader(labels_path='labels.csv', img_dir=IMG_DIR)

    def test_generate_splits(self):
        # Case 1: default 80/20 ratio
        train_idx, valid_idx = self._loader._splits_indices
        total = len(self._loader._df)
        expected_train = int(0.8 * total)
        expected_valid = ceil(0.2 * total)
        self.assertEqual(expected_train, len(train_idx),
                         msg=f'Expected: {expected_train} train count; result: {len(train_idx)}')
        self.assertEqual(expected_valid, len(valid_idx),
                         msg=f'Expected: {expected_valid} valid count; result: {len(valid_idx)}')
        # Case 2: 50/50 ratio
        train_idx, valid_idx = self._loader._generate_splits(split_size=0.50)
        total = len(self._loader._df)
        expected_train = int(0.5 * total)
        expected_valid = ceil(0.5 * total)
        self.assertEqual(expected_train, len(train_idx),
                         msg=f'Expected: {expected_train} train count; result: {len(train_idx)}')
        self.assertEqual(expected_valid, len(valid_idx),
                         msg=f'Expected: {expected_valid} valid count; result: {len(valid_idx)}')

    def test_get_data_loaders(self):
        loaders = self._loader.get_data_loaders()
        # Verify return dict with two keys: train & validation
        self.assertEqual(2, len(loaders),
                         msg=f'Expected 2; result: {len(loaders)}')
        for key in ['train', 'validation']:
            self.assertTrue(key in loaders,
                            msg=f'{key} not in {loaders.keys()}')

        # Assess size of each loader: more than or equal to data subset size
        expected = len(self._loader._train_df)
        max_loader_count = len(loaders['train']) * 32
        self.assertLessEqual(expected, max_loader_count,
                             msg=f'Expected: {expected}; result: {max_loader_count}')
        expected = len(self._loader._validation_df)
        max_loader_count = len(loaders['validation']) * 32
        self.assertLessEqual(expected, max_loader_count,
                            msg=f'Expected: {expected}; result: {max_loader_count}')

    def test_show_sample_images(self):
        """No unit cases, just visual check."""
        self._loader.show_sample_images()


if __name__ == '__main__':
    unittest.main()
