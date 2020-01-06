```mermaid
graph LR
N140[DCG,discounted_cumulative_gain,discounted_cumulative_gain_measure]
N155[N/A]
N0[data_science]
N4[classification]
N7[F1]
N13[neural_networks]
N30[N/A]
N149[N/A]
N152[N/A]
N11[frequent_itemset_mining]
N21[matrix_factorization]
N82[topic_model,topic_models]
N106[SGD,stochastic_gradient_descent]
N9[clustering]
N10[density-based_clustering]
N35[recommendation,recommender_systems]
N38[tensor_decomposition,tensor_factorization]
N41[decision_tree,decision_trees]
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
N132[MLE,maximum_likelihood_estimation]
N136[NMF,non-negative_matrix_factorization,non_negative_matrix_factorization,nonnegative_matrix_factorization]
N139[SVR,support_vector_regression]
N143[FPR,false-positive_rate,false_positive_rate]
N148[AUC,area_under_curve,area_under_the_curve]
N156[accuracy]
N157[N/A]
N159[PCA,principal_component_analysis,principal_components_analysis]
N162[TPR,true_positive_rate]
N107[support_vector_machine,support_vector_machines,svm,svms]
N1[data_mining]
N2[machine_learning]
N6[binary_classification]
N12[apriori]
N14[perceptron]
N23[artificial_neural_networks]
N25[constrained_stochastic_gradient_descent]
N28[sensitivity]
N29[specificity]
N44[ensemble,ensembles]
N53[macro-f1,macro_f1]
N55[micro-f1,micro_f1]
N91[LDA,latent_dirichlet_allocation]
N99[MAP,mean_average_precision]
N113[MRR,mean_reciprocal_rank]
N116[MAE,mean_absolute_error]
N119[NDCG,normalized_discounted_cumulative_gain,normalized_discounted_cumulative_gain_measure]
N122[NB,naive_bayes]
N134[RMSE,root-mean-square_error,root_mean_square_error,root_mean_squared_error]
N146[PMF,probabilistic_matrix_factorization]
N150[bagging]
N151[boosting]
N154[logistic_regression]
N20[least_squares_support_vector_machine]
N140 --> |child| N119
N140 --> |child| N99
N140 --> |child| N113
N155 --> |child| N122
N155 --> |child| N107
N155 --> |child| N154
N0 --> |child| N1
N0 --> |child| N2
N4 --> |child| N6
N4 --> |child| N44
N7 --> |child| N55
N7 --> |child| N53
N13 --> |child| N14
N13 --> |child| N23
N30 --> |child| N28
N30 --> |child| N29
N149 --> |child| N116
N149 --> |child| N134
N152 --> |child| N150
N152 --> |child| N151
N11 --> |child| N12
N21 --> |child| N146
N82 --> |child| N91
N106 --> |child| N25
N9 --> |algorithms| N10
N9 --> |algorithms| N50
N157 --> |measures| N7
N157 --> |measures| N140
N157 --> |measures| N86
N157 --> |measures| N87
N157 --> |measures| N156
N107 --> |child| N20
N1 --> |tasks| N9
N1 --> |tasks| N64
N1 --> |tasks| N4
N2 --> |models| N74
N2 --> |models| N85
N2 --> |models| N72
```
