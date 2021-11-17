import torch
import torchvision

from PIL import Image


class Predictor:
    """
    Predict the music mood by the input spectrogram
    """

    def __init__(self, trained_weights_path):
        """
        Initialize the Predictor by the trained data information

        Args:
            trained_weights_path: the trained weights data file path
        """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = torchvision.models.resnet18()
        # Change the last layer shape
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_features, 4)
        # Put trained weights
        self.model.load_state_dict(torch.load(trained_weights_path, map_location=torch.device(self.device)))
        self.model.eval()
        # Mood class names
        self.class_names = ["angry", "happy", "relaxed", "sad"]
        # Compose transformers and normalize it
        self.loader = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                                      torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                                                                       std=[0.229, 0.224, 0.225])])

    @staticmethod
    def map_from_idx(array, map_list):
        """
        Function that takes an array of indices positions and returns
        the elements at these specific positions in map_list
        """
        res = []
        for i in array:
            res.append(map_list[int(i)])
        return res

    def predict(self, img_path, k=2):
        """
        Predict the music mood by it's spectrogram

        Args:
            img_path: test image file, .jpg format expected
            k: top k

        Returns:
            the predicted mood class and its corresponding probability in dict
        """
        img = Image.open(img_path)
        img = self.loader(img).unsqueeze(0).to(self.device)
        self.model.eval()
        output = self.model(img)
        probability, class_idx = torch.topk(output, k)
        probability = probability[0].detach().numpy()
        class_idx = class_idx[0].detach().numpy()
        class_val = self.map_from_idx(class_idx, self.class_names)
        mood = {}
        for i in range(k):
            mood[class_val[i]] = probability[i]
        return mood
