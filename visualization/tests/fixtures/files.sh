while read -r file; do
  dir="$(dirname "$file")"
  mkdir -p "$dir"
  touch "$file"
done <<EOF
analysis_root/merge/eval/P-1_W-B1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3__cell_mapping_stats.tsv
analysis_root/merge/eval/P-3_W-B2__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-A1__channel_min_histogram.png
analysis_root/merge/eval/P-2__sbs_to_ph_matching_rates.png
analysis_root/merge/eval/P-2_W-A3__deduplication_stats.tsv
analysis_root/merge/eval/P-1__sbs_to_ph_matching_rates.tsv
analysis_root/merge/eval/P-2_W-B1__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2_W-A2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-B1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B2__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-B2__deduplication_stats.tsv
analysis_root/merge/eval/P-3__sbs_to_ph_matching_rates.png
analysis_root/merge/eval/P-1_W-A3__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A1__deduplication_stats.tsv
analysis_root/merge/eval/P-3__sbs_to_ph_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A1__deduplication_stats.tsv
analysis_root/merge/eval/P-1_W-A3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A2__deduplication_stats.tsv
analysis_root/merge/eval/P-1_W-A2__deduplication_stats.tsv
analysis_root/merge/eval/P-1_W-B1__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-B2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2__all_cells_by_channel_min.png
analysis_root/merge/eval/P-1_W-A1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A3__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-A2__channel_min_histogram.png
analysis_root/merge/eval/P-2_W-B1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-3_W-B1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-3_W-B2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2_W-B1__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-A2__deduplication_stats.tsv
analysis_root/merge/eval/P-3_W-B2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-2_W-A3__channel_min_histogram.png
analysis_root/merge/eval/P-1_W-B2__channel_min_histogram.png
analysis_root/merge/eval/P-1_W-A2__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A3__channel_min_histogram.png
analysis_root/merge/eval/P-1__cells_with_channel_min_0.png
analysis_root/merge/eval/P-2_W-A3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-2_W-A2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2_W-B3__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-A1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B1__channel_min_histogram.png
analysis_root/merge/eval/P-2_W-A1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A2__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-B1__deduplication_stats.tsv
analysis_root/merge/eval/P-3__cells_with_channel_min_0.png
analysis_root/merge/eval/P-3_W-B3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-2__sbs_to_ph_matching_rates.tsv
analysis_root/merge/eval/P-3_W-B3__deduplication_stats.tsv
analysis_root/merge/eval/P-2_W-A1__deduplication_stats.tsv
analysis_root/merge/eval/P-3_W-B3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B3__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-B1__channel_min_histogram.png
analysis_root/merge/eval/P-2__cell_mapping_stats.tsv
analysis_root/merge/eval/P-2_W-B3__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A3__deduplication_stats.tsv
analysis_root/merge/eval/P-1__ph_to_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1_W-A1__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A1__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-A3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2_W-A3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-2_W-B1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-2_W-B3__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1__all_cells_by_channel_min.png
analysis_root/merge/eval/P-2_W-B2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-B3__channel_min_histogram.png
analysis_root/merge/eval/P-3_W-B2__channel_min_histogram.png
analysis_root/merge/eval/P-3__ph_to_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1__cell_mapping_stats.tsv
analysis_root/merge/eval/P-1__ph_to_sbs_matching_rates.png
analysis_root/merge/eval/P-2__ph_to_sbs_matching_rates.png
analysis_root/merge/eval/P-2_W-B2__channel_min_histogram.png
analysis_root/merge/eval/P-2_W-B3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B3__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-2__ph_to_sbs_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B3__deduplication_stats.tsv
analysis_root/merge/eval/P-1__sbs_to_ph_matching_rates.png
analysis_root/merge/eval/P-3__all_cells_by_channel_min.png
analysis_root/merge/eval/P-2__cells_with_channel_min_0.png
analysis_root/merge/eval/P-1_W-A2__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A1__final_phenotype_matching_rates.tsv
analysis_root/merge/eval/P-1_W-B2__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3_W-A1__final_sbs_matching_rates.tsv
analysis_root/merge/eval/P-3__ph_to_sbs_matching_rates.png
analysis_root/sbs_test/eval/mapping/P-1__read_mapping_heatmap.png
analysis_root/sbs_test/eval/mapping/P-1__mapping_vs_threshold_qmin.png
analysis_root/sbs_test/eval/mapping/P-1__cell_mapping_heatmap_one.png
analysis_root/sbs_test/eval/mapping/P-1__reads_per_cell_histogram.png
analysis_root/sbs_test/eval/mapping/P-1__mapping_vs_threshold_peak.png
analysis_root/sbs_test/eval/mapping/P-1__cell_mapping_heatmap_any.png
analysis_root/sbs_test/eval/mapping/P-1__gene_symbol_histogram.png
analysis_root/sbs_test/eval/mapping/P-1__mapping_overview.tsv
analysis_root/sbs_test/eval/mapping/P-1__cell_mapping_heatmap_any.tsv
analysis_root/sbs_test/eval/mapping/P-1__cell_mapping_heatmap_one.tsv
analysis_root/sbs_test/eval/segmentation/P-1__cell_density_heatmap.tsv
analysis_root/sbs_test/eval/segmentation/P-1__cell_density_heatmap.png
analysis_root/sbs_test/eval/segmentation/P-1__segmentation_overview.tsv
analysis_root/sbs/eval/mapping/P-3__cell_mapping_heatmap_one.tsv
analysis_root/sbs/eval/mapping/P-1__read_mapping_heatmap.png
analysis_root/sbs/eval/mapping/P-2__cell_mapping_heatmap_any.tsv
analysis_root/sbs/eval/mapping/P-3__reads_per_cell_histogram.png
analysis_root/sbs/eval/mapping/P-3__mapping_vs_threshold_peak.png
analysis_root/sbs/eval/mapping/P-3__mapping_vs_threshold_qmin.png
analysis_root/sbs/eval/mapping/P-3__cell_mapping_heatmap_any.png
analysis_root/sbs/eval/mapping/P-2__read_mapping_heatmap.png
analysis_root/sbs/eval/mapping/P-2__cell_mapping_heatmap_any.png
analysis_root/sbs/eval/mapping/P-1__mapping_vs_threshold_qmin.png
analysis_root/sbs/eval/mapping/P-2__gene_symbol_histogram.png
analysis_root/sbs/eval/mapping/P-3__cell_mapping_heatmap_any.tsv
analysis_root/sbs/eval/mapping/P-1__cell_mapping_heatmap_one.png
analysis_root/sbs/eval/mapping/P-1__reads_per_cell_histogram.png
analysis_root/sbs/eval/mapping/P-2__cell_mapping_heatmap_one.png
analysis_root/sbs/eval/mapping/P-2__cell_mapping_heatmap_one.tsv
analysis_root/sbs/eval/mapping/P-1__mapping_vs_threshold_peak.png
analysis_root/sbs/eval/mapping/P-1__cell_mapping_heatmap_any.png
analysis_root/sbs/eval/mapping/P-2__mapping_overview.tsv
analysis_root/sbs/eval/mapping/P-1__gene_symbol_histogram.png
analysis_root/sbs/eval/mapping/P-3__mapping_overview.tsv
analysis_root/sbs/eval/mapping/P-2__reads_per_cell_histogram.png
analysis_root/sbs/eval/mapping/P-2__mapping_vs_threshold_qmin.png
analysis_root/sbs/eval/mapping/P-2__mapping_vs_threshold_peak.png
analysis_root/sbs/eval/mapping/P-1__mapping_overview.tsv
analysis_root/sbs/eval/mapping/P-3__gene_symbol_histogram.png
analysis_root/sbs/eval/mapping/P-1__cell_mapping_heatmap_any.tsv
analysis_root/sbs/eval/mapping/P-1__cell_mapping_heatmap_one.tsv
analysis_root/sbs/eval/mapping/P-3__cell_mapping_heatmap_one.png
analysis_root/sbs/eval/mapping/P-3__read_mapping_heatmap.png
analysis_root/sbs/eval/segmentation/P-1__cell_density_heatmap.tsv
analysis_root/sbs/eval/segmentation/P-1__cell_density_heatmap.png
analysis_root/sbs/eval/segmentation/P-2__cell_density_heatmap.tsv
analysis_root/sbs/eval/segmentation/P-2__segmentation_overview.tsv
analysis_root/sbs/eval/segmentation/P-1__segmentation_overview.tsv
analysis_root/sbs/eval/segmentation/P-2__cell_density_heatmap.png
analysis_root/sbs/eval/segmentation/P-3__cell_density_heatmap.png
analysis_root/sbs/eval/segmentation/P-3__cell_density_heatmap.tsv
analysis_root/sbs/eval/segmentation/P-3__segmentation_overview.tsv
analysis_root/phenotype/eval/features/P-2__cell_WGA_min_heatmap.png
analysis_root/phenotype/eval/features/P-1__cell_DAPI_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-2__cell_COXIV_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-1__cell_DAPI_min_heatmap.png
analysis_root/phenotype/eval/features/P-1__cell_CENPA_min_heatmap.png
analysis_root/phenotype/eval/features/P-1__cell_COXIV_min_heatmap.png
analysis_root/phenotype/eval/features/P-2__cell_COXIV_min_heatmap.png
analysis_root/phenotype/eval/features/P-3__cell_DAPI_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-3__cell_CENPA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-1__cell_CENPA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-1__cell_WGA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-3__cell_COXIV_min_heatmap.png
analysis_root/phenotype/eval/features/P-2__cell_DAPI_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-3__cell_COXIV_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-2__cell_CENPA_min_heatmap.png
analysis_root/phenotype/eval/features/P-2__cell_WGA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-3__cell_CENPA_min_heatmap.png
analysis_root/phenotype/eval/features/P-3__cell_WGA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-2__cell_DAPI_min_heatmap.png
analysis_root/phenotype/eval/features/P-3__cell_DAPI_min_heatmap.png
analysis_root/phenotype/eval/features/P-1__cell_WGA_min_heatmap.png
analysis_root/phenotype/eval/features/P-1__cell_COXIV_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-2__cell_CENPA_min_heatmap.tsv
analysis_root/phenotype/eval/features/P-3__cell_WGA_min_heatmap.png
analysis_root/phenotype/eval/segmentation/P-1__cell_density_heatmap.tsv
analysis_root/phenotype/eval/segmentation/P-1__cell_density_heatmap.png
analysis_root/phenotype/eval/segmentation/P-2__cell_density_heatmap.tsv
analysis_root/phenotype/eval/segmentation/P-2__segmentation_overview.tsv
analysis_root/phenotype/eval/segmentation/P-1__segmentation_overview.tsv
analysis_root/phenotype/eval/segmentation/P-2__cell_density_heatmap.png
analysis_root/phenotype/eval/segmentation/P-3__segmentation_overview.tsv
analysis_root/aggregate_old/eval/nuclear_feature_violins.png
analysis_root/aggregate_old/eval/interphase_missing.tsv
analysis_root/aggregate_old/eval/cell_feature_violins.png
analysis_root/aggregate_old/eval/all_missing.tsv
analysis_root/aggregate_old/eval/mitotic_missing.tsv
analysis_root/aggregate_old/eval/mitotic_stats.tsv
EOF
