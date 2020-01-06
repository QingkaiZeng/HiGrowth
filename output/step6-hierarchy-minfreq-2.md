```mermaid
graph LR
N0[data_science]
N140[DCG,discounted_cumulative_gain,discounted_cumulative_gain_measure]
N13[neural_networks]
N149[N/A]
N221[F1,f-measure,f1-measure]
N82[topic_model,topic_models]
N106[SGD,stochastic_gradient_descent]
N107[support_vector_machine,support_vector_machines,svm,svms]
N4[classification]
N6[binary_classification]
N9[clustering]
N10[density-based_clustering]
N11[frequent_itemset_mining]
N12[apriori]
N21[matrix_factorization]
N28[sensitivity]
N29[specificity]
N38[tensor_decomposition,tensor_factorization]
N41[decision_tree,decision_trees]
N44[ensemble,ensembles]
N50[k-means,k-means_clustering]
N62[random_forest,random_forests]
N64[regression,regression_analysis]
N72[semi-supervised,semi-supervised_learning,semi_supervised_learning]
N74[supervised,supervised_learning]
N85[unsupervised,unsupervised_learning]
N86[precision]
N87[recall]
N96[SVD,singular_value_decomposition]
N110[NMI,normalized_mutual_information]
N122[NB,naive_bayes]
N132[MLE,maximum_likelihood_estimation]
N136[NMF,non-negative_matrix_factorization,non_negative_matrix_factorization,nonnegative_matrix_factorization]
N139[SVR,support_vector_regression]
N143[FPR,false-positive_rate,false_positive_rate]
N146[PMF,probabilistic_matrix_factorization]
N148[AUC,area_under_curve,area_under_the_curve]
N150[bagging]
N151[boosting]
N154[logistic_regression]
N156[accuracy]
N159[PCA,principal_component_analysis,principal_components_analysis]
N162[TPR,true_positive_rate]
N169[C4.5]
N170[association_rule_mining]
N171[hierarchical_clustering]
N172[community_detection]
N173[document_clustering]
N174[outlier_detection]
N176[anomaly_detection]
N177[GSP]
N178[prefixspan]
N180[link_prediction]
N183[k_nearest_neighbor,knn]
N184[spectral_clustering]
N185[dimensionality_reduction]
N187[CART]
N192[dbscan]
N193[feature_selection]
N194[sequential_pattern_mining]
N195[link_recommendation]
N197[feature_extraction]
N198[fp-growth]
N200[k-medoids]
N202[text_categorization]
N203[information_gain]
N204[similarity_search]
N205[linear_regression]
N206[adaboost]
N207[f-score]
N209[eclat]
N210[bayesian_networks]
N211[SPADE]
N212[gini_index]
N214[linear_svm]
N216[f1_measure]
N219[N/A]
N1[data_mining]
N2[machine_learning]
N14[perceptron]
N23[artificial_neural_networks]
N35[recommendation,recommender_systems]
N53[macro-f1,macro_f1]
N55[micro-f1,micro_f1]
N91[LDA,latent_dirichlet_allocation]
N99[MAP,mean_average_precision]
N113[MRR,mean_reciprocal_rank]
N116[MAE,mean_absolute_error]
N119[NDCG,normalized_discounted_cumulative_gain,normalized_discounted_cumulative_gain_measure]
N134[RMSE,root-mean-square_error,root_mean_square_error,root_mean_squared_error]
N168[knowledge_discovery]
N189[visualization]
N191[CSGD,constrained_stochastic_gradient_descent]
N196[artificial_intelligence]
N223[least_squares_support_vector_machine,ls-svm]
N0 --> |child| N1
N0 --> |child| N2
N0 --> |child| N168
N0 --> |child| N189
N0 --> |child| N196
N0 --> |child| N35
N140 --> |child| N119
N140 --> |child| N99
N140 --> |child| N113
N13 --> |child| N14
N13 --> |child| N23
N149 --> |child| N116
N149 --> |child| N134
N221 --> |child| N55
N221 --> |child| N53
N82 --> |descendant| N91
N106 --> |child| N191
N107 --> |child| N223
N4 --> |applications| N6
N4 --> |algorithms| N44
N4 --> |algorithms| N122
N4 --> |algorithms| N41
N4 --> |algorithms| N107
N4 --> |algorithms| N154
N4 --> |algorithms| N13
N4 --> |algorithms| N169
N4 --> |algorithms| N183
N4 --> |algorithms| N187
N4 --> |algorithms| N62
N4 --> |applications| N202
N4 --> |algorithms| N210
N4 --> |algorithms| N214
N9 --> |algorithms| N10
N9 --> |algorithms| N50
N9 --> |algorithms| N171
N9 --> |algorithms| N184
N9 --> |algorithms| N192
N9 --> |algorithms| N136
N9 --> |algorithms| N200
N9 --> |algorithms| N96
N10 --> |algorithms| N192
N11 --> |algorithms| N12
N11 --> |algorithms| N198
N11 --> |algorithms| N209
N21 --> |techniques| N146
N21 --> |techniques| N96
N21 --> |techniques| N136
N44 --> |methods| N150
N44 --> |methods| N151
N64 --> |algorithms| N205
N85 --> |algorithms| N50
N151 --> |methods| N206
N185 --> |methods| N159
N193 --> |measures| N203
N193 --> |measures| N212
N194 --> |algorithms| N177
N194 --> |algorithms| N178
N194 --> |algorithms| N211
N219 --> |measures| N140
N219 --> |measures| N28
N219 --> |measures| N110
N219 --> |measures| N207
N219 --> |measures| N148
N219 --> |measures| N86
N219 --> |measures| N87
N219 --> |measures| N216
N219 --> |measures| N156
N219 --> |measures| N29
N219 --> |measures| N221
N1 --> |tasks| N9
N1 --> |tasks| N64
N1 --> |tasks| N4
N1 --> |tasks| N170
N1 --> |tasks| N172
N1 --> |tasks| N173
N1 --> |tasks| N174
N1 --> |tasks| N176
N1 --> |tasks| N180
N1 --> |tasks| N185
N1 --> |tasks| N193
N1 --> |tasks| N195
N1 --> |tasks| N11
N1 --> |tasks| N197
N1 --> |tasks| N194
N1 --> |tasks| N204
N2 --> |models| N74
N2 --> |models| N85
N2 --> |models| N72
```
