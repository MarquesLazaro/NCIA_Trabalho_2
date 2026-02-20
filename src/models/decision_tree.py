from sklearn.tree import DecisionTreeClassifier


class DecisionTreeModel(DecisionTreeClassifier):
    def __init__(self, random_state=42):
        super().__init__(
            criterion="gini",
            splitter="best",
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=random_state,
        )
