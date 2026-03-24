# Deduplication Evaluation Report

## Evaluation Logic Overview

This evaluation logic evaluates the performance of a deduplication process by comparing an **original dataset** with a **deduplicated dataset**.

### 1. Fingerprint Generation

- **Key Columns**: Generates a fingerprint based on selected fields (e.g., Full Name, Email, Company, Course).
- **Normalization**: Fingerprints are constructed by concatenating valid, normalized field values to ensure similar records produce identical identifiers

### 2. Determining Ground Truth

The script counts how many times each fingerprint appears in the original dataset:

- **Duplicates**: Records with the same fingerprint appearing more than once.
- **Unique**: Records appearing only once.

### 3. Comparison and Classification

The script compares fingerprints against the deduplicated dataset using the following logic:

- **True Positive (TP)**: A duplicate record is correctly retained.
- **False Negative (FN)**: A duplicate record is incorrectly removed.
- **True Negative (TN)**: A unique record is correctly retained.
- **False Positive (FP)**: A unique record is incorrectly removed.

### 4. Metrics Reporting

Finally, the script computes **Precision** and **Recall**, reporting the total classification results and the expected size of the deduplicated dataset.

## Deduplication Agent Evaluation Results (Based on Threshold Tuning)

![Evaluation Result](./img/evaluation-result.png)

Since the threshold below 0.98 shows a linear increase, we evaluate the threshold between 0.98 and 0.99, while the threshold above 0.99 shows a linear decrease. Therefore, we initially speculate that the optimal threshold is between 0.98 and 0.99. Based on experimental results at different thresholds, the deduplication agent exhibits a typical trade-off between Precision and Recall, with an overall stable upward trend.

The graph shows that precision increases steadily with the threshold, from 0.44 at 0.980 to 0.83 at 0.990. This indicates that the model significantly reduces false positives (FP) at higher thresholds, making more conservative and accurate judgments. Recall also increases with the threshold, from 0.61 to 0.92, demonstrating that the model's ability to identify duplicate data improves simultaneously, reducing false negatives (FN).

Based on experimental data, the overall model performance improved significantly, with precision and recall showing a synchronous upward trend. This phenomenon indicates that the current feature engineering design and similarity measurement function are effective in distinguishing target samples and have not yet reached a performance saturation bottleneck, reflecting the model's potential for further optimization.

### Optimal Threshold Range

In threshold sensitivity analysis, [0.985, 0.988] was determined to be the optimal value range. Specific performance balance is as follows:

- **Equilibrium Point Analysis:**

  When the threshold is set to 0.985, P ≈ 0.63 and R ≈ 0.78, achieving a preliminary balance between the two metrics.

- **High Recall Tendency:**

  As the threshold increases to 0.988, precision increases to 0.74, and recall increases synchronously to 0.89. This configuration is suitable for business scenarios with low tolerance for missed detections.

- **Peak Performance and Risk Warning:**

  When the threshold was further increased to 0.990, the model achieved optimal statistical performance (P ≈ 0.83, R ≈ 0.92). However, it is crucial to be aware of the risk of semantic overfitting that may result from excessively high thresholds, i.e., the model might over-capture subtle similarities, thus mistakenly clustering and merging non-repeating entities. Manual verification showed that this risk did not occur at 0.990. Above the threshold of 0.990, an increased false negative rate was observed.

### Conclusions and Improvement Suggestions

The current deduplication agent exhibits stable and consistent performance growth during threshold increases, indicating that the current deduplication strategy is effective.

### Limitations of Test Data

Since the test data was dummy data provided by BlackBerry CCoE, the main deduplication metrics considered in general tests (full name, email, phone number, etc.) were encrypted and anonymized, and therefore cannot be used as the main features for deduplication in this project. Consequently, the results of this project differ significantly from those in actual production, requiring further modifications and improvements.
