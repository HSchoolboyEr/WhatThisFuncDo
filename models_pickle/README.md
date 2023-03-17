
## Results


| Number | Model Type                                 | TRAIN Score_f1 (macro) | TRAIN Score_f1 (micro) | TEST Score_f1 (micro) |
|:--------:|:--------------------------------------------:|:------------:|:--------------:|:-----------------------:|
| 1      | `LogisticRegression` CountVectorizer, bow 1-2 |            | 0.7651174066634342 ||
| 2      | `LogisticRegression` TF-IDF, bow 1-2       |            | 0.7815335596037958 ||
| 3      | `LogisticRegression` CountVectorizer, bow 1-3 |            | 0.8483757013229895 |0.7364315892102697|
| 4      | `LogisticRegression` TF-IDF, bow 1-3       |            | 0.8447045785135416 ||
| 5      | `DescisionTree`                            | 0.8669249360756363 | 0.9079448638913902 ||
| 6      | `RandomForest`                             | 0.907964543683028 | 0.9482579483272148 |0.8664819944598338|
| 7      | `CatBoostClassifier`                       | ...        | ...          ||
| 8      | `XGBClassifier`                            | 0.9054175084247906 | 0.9431322296876082 ||
| 9      | `LGBMClassifier`                           | 0.9074649666973832 | 0.9463877536884394 ||
| 10      | `StackingClassifier` models 5,6,8,9 by LogReg | 0.9064061493700429 |   0.9459028884117199 |                       |
| 11      | `-`                                        |            |              |                       |
