# =============================================================================
# Generate Figures for Rhetoric of Decks Presentation
# Data on Returns to Education and Skill-Biased Technological Change
# =============================================================================

library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)

# Set seed for reproducibility
set.seed(42)

# Define a beautiful, professional color palette
palette_main <- c(
  "primary" = "#2E4057",      # Deep navy blue

"secondary" = "#048A81",    # Teal
  "accent" = "#E85D04",       # Warm orange
  "highlight" = "#9D4EDD",    # Purple
  "neutral" = "#6C757D",      # Gray
  "female" = "#D62828",       # Deep red
  "male" = "#003049",         # Dark blue
  "college" = "#2E4057",      # Navy
  "highschool" = "#048A81",   # Teal
  "lesshs" = "#E85D04"        # Orange
)

# Custom theme for all plots
theme_rhetoric <- function(base_size = 14) {
  theme_minimal(base_size = base_size) +
    theme(
      text = element_text(color = "#2E4057"),
      plot.title = element_text(size = rel(1.3), face = "bold",
                                hjust = 0, margin = margin(b = 15)),
      plot.subtitle = element_text(size = rel(1.0), color = "#6C757D",
                                   hjust = 0, margin = margin(b = 20)),
      plot.caption = element_text(size = rel(0.75), color = "#6C757D",
                                  hjust = 1, margin = margin(t = 15)),
      axis.title = element_text(size = rel(0.95), face = "bold"),
      axis.title.x = element_text(margin = margin(t = 12)),
      axis.title.y = element_text(margin = margin(r = 12)),
      axis.text = element_text(size = rel(0.9), color = "#2E4057"),
      panel.grid.major = element_line(color = "#E9ECEF", linewidth = 0.4),
      panel.grid.minor = element_blank(),
      legend.position = "bottom",
      legend.title = element_text(face = "bold", size = rel(0.9)),
      legend.text = element_text(size = rel(0.85)),
      legend.key.width = unit(1.5, "cm"),
      plot.margin = margin(20, 25, 20, 25),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# =============================================================================
# Figure 1: College Wage Premium Over Time (1915-2020)
# Based on Goldin & Katz data patterns
# =============================================================================

years <- 1915:2020
n <- length(years)

# Create realistic college wage premium pattern
# U-shaped pattern: high in early 20th century, compressed mid-century, rises again
college_premium <- numeric(n)
for (i in 1:n) {
  year <- years[i]
  if (year <= 1940) {
    # Early period: gradual decline from ~65% to ~45%
    college_premium[i] <- 0.65 - 0.005 * (year - 1915) + rnorm(1, 0, 0.02)
  } else if (year <= 1950) {
    # WWII compression
    college_premium[i] <- 0.45 - 0.01 * (year - 1940) + rnorm(1, 0, 0.02)
  } else if (year <= 1980) {
    # Post-war stability, slight decline
    college_premium[i] <- 0.40 - 0.002 * (year - 1950) + rnorm(1, 0, 0.015)
  } else {
    # SBTC era: rapid increase
    college_premium[i] <- 0.35 + 0.012 * (year - 1980) + rnorm(1, 0, 0.01)
  }
}

df_premium <- data.frame(
  year = years,
  premium = college_premium * 100  # Convert to percentage
)

# Smooth the data slightly
df_premium$premium_smooth <- stats::filter(df_premium$premium, rep(1/5, 5), sides = 2)
df_premium$premium_smooth[is.na(df_premium$premium_smooth)] <- df_premium$premium[is.na(df_premium$premium_smooth)]

p1 <- ggplot(df_premium, aes(x = year, y = premium_smooth)) +
  # Add shaded regions for key periods
  annotate("rect", xmin = 1980, xmax = 2020, ymin = -Inf, ymax = Inf,
           fill = "#E85D04", alpha = 0.08) +
  annotate("rect", xmin = 1940, xmax = 1950, ymin = -Inf, ymax = Inf,
           fill = "#048A81", alpha = 0.08) +
  # Main line
  geom_line(linewidth = 1.3, color = palette_main["primary"]) +
  # Key annotations
  annotate("text", x = 1945, y = 70, label = "WWII\nCompression",
           size = 3.2, color = "#048A81", fontface = "italic", hjust = 0.5) +
  annotate("text", x = 2000, y = 45, label = "SBTC Era",
           size = 3.5, color = "#E85D04", fontface = "bold", hjust = 0.5) +
  # Arrow pointing to the rise
  annotate("segment", x = 1982, xend = 1990, y = 38, yend = 42,
           arrow = arrow(length = unit(0.2, "cm")), color = "#E85D04", linewidth = 0.8) +
  scale_x_continuous(breaks = seq(1920, 2020, 20), limits = c(1915, 2020)) +
  scale_y_continuous(labels = function(x) paste0(round(x), "%"),
                     limits = c(30, 75)) +
  labs(
    title = "The College Wage Premium: A Century of Change",
    subtitle = "Log wage differential between college and high school graduates",
    x = "Year",
    y = "College Wage Premium",
    caption = "Pattern based on Goldin & Katz (2008). Shaded regions indicate key structural shifts."
  ) +
  theme_rhetoric()

ggsave("figures/fig1_college_premium.pdf", p1, width = 10, height = 6.5)
ggsave("figures/fig1_college_premium.png", p1, width = 10, height = 6.5, dpi = 300)

# =============================================================================
# Figure 2: Gender Gap in Labor Force Participation by Education
# =============================================================================

years2 <- seq(1950, 2020, 5)

# Female LFP by education (increasing over time, faster for more educated)
lfp_data <- data.frame(
  year = rep(years2, 3),
  education = rep(c("Less than High School", "High School", "College+"), each = length(years2)),
  female_lfp = c(
    # Less than HS: slower increase, plateaus
    34 + 0.3 * (years2 - 1950) - 0.004 * (years2 - 1950)^2 + rnorm(length(years2), 0, 1.5),
    # High School: moderate increase
    38 + 0.5 * (years2 - 1950) - 0.002 * (years2 - 1950)^2 + rnorm(length(years2), 0, 1.5),
    # College+: strong increase
    45 + 0.65 * (years2 - 1950) - 0.001 * (years2 - 1950)^2 + rnorm(length(years2), 0, 1.5)
  )
)

# Cap at realistic values
lfp_data$female_lfp <- pmin(pmax(lfp_data$female_lfp, 25), 82)

# Set factor levels for proper ordering
lfp_data$education <- factor(lfp_data$education,
                             levels = c("College+", "High School", "Less than High School"))

p2 <- ggplot(lfp_data, aes(x = year, y = female_lfp, color = education)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2.5, alpha = 0.7) +
  # Direct labels instead of legend
  annotate("text", x = 2022, y = 80, label = "College+",
           color = "#2E4057", fontface = "bold", hjust = 0, size = 3.8) +
  annotate("text", x = 2022, y = 68, label = "High School",
           color = "#048A81", fontface = "bold", hjust = 0, size = 3.8) +
  annotate("text", x = 2022, y = 42, label = "< High School",
           color = "#E85D04", fontface = "bold", hjust = 0, size = 3.8) +
  scale_color_manual(values = c("College+" = "#2E4057",
                                "High School" = "#048A81",
                                "Less than High School" = "#E85D04")) +
  scale_x_continuous(breaks = seq(1950, 2020, 10), limits = c(1950, 2030)) +
  scale_y_continuous(labels = function(x) paste0(x, "%"), limits = c(25, 85)) +
  labs(
    title = "The Education-Participation Revolution",
    subtitle = "Female labor force participation rate by educational attainment",
    x = "Year",
    y = "Labor Force Participation Rate",
    caption = "Data patterns based on CPS and historical Census records."
  ) +
  theme_rhetoric() +
  theme(legend.position = "none")

ggsave("figures/fig2_lfp_education.pdf", p2, width = 10, height = 6.5)
ggsave("figures/fig2_lfp_education.png", p2, width = 10, height = 6.5, dpi = 300)

# =============================================================================
# Figure 3: Event Study - Effect of Computer Adoption on Wages
# Simulated policy/technology shock event study
# =============================================================================

# Event time from -10 to +10 years
event_time <- -10:10
n_event <- length(event_time)

# Pre-treatment: flat around zero
# Post-treatment: gradual increase
event_effects <- numeric(n_event)
event_se <- numeric(n_event)

for (i in 1:n_event) {
  t <- event_time[i]
  if (t < 0) {
    # Pre-treatment: should be near zero (parallel trends)
    event_effects[i] <- rnorm(1, 0, 0.008)
    event_se[i] <- 0.025 + abs(t) * 0.002
  } else if (t == 0) {
    # Treatment year
    event_effects[i] <- 0.02 + rnorm(1, 0, 0.005)
    event_se[i] <- 0.025
  } else {
    # Post-treatment: gradual increase, then leveling
    event_effects[i] <- 0.02 + 0.015 * log(t + 1) + rnorm(1, 0, 0.005)
    event_se[i] <- 0.022 + t * 0.001
  }
}

df_event <- data.frame(
  event_time = event_time,
  effect = event_effects,
  se = event_se,
  ci_lower = event_effects - 1.96 * event_se,
  ci_upper = event_effects + 1.96 * event_se
)

p3 <- ggplot(df_event, aes(x = event_time, y = effect)) +
  # Zero reference line
  geom_hline(yintercept = 0, linetype = "dashed", color = "#6C757D", linewidth = 0.6) +
  # Treatment time indicator
  geom_vline(xintercept = -0.5, linetype = "solid", color = "#E85D04", linewidth = 0.8, alpha = 0.7) +
  # Confidence interval ribbon
  geom_ribbon(aes(ymin = ci_lower, ymax = ci_upper), fill = palette_main["primary"], alpha = 0.2) +
  # Point estimates
  geom_point(size = 3, color = palette_main["primary"]) +
  geom_line(linewidth = 0.8, color = palette_main["primary"]) +
  # Annotations
  annotate("text", x = -5, y = 0.09, label = "Pre-treatment:\nParallel trends",
           size = 3.5, color = "#6C757D", fontface = "italic") +
  annotate("text", x = 5, y = 0.09, label = "Post-treatment:\nDiverging outcomes",
           size = 3.5, color = palette_main["primary"], fontface = "italic") +
  annotate("text", x = 0.5, y = -0.055, label = "Treatment",
           size = 3.2, color = "#E85D04", fontface = "bold", hjust = 0) +
  scale_x_continuous(breaks = seq(-10, 10, 2)) +
  scale_y_continuous(labels = function(x) paste0(round(x * 100, 1), "%"),
                     limits = c(-0.06, 0.11)) +
  labs(
    title = "Computer Adoption and the College Wage Premium",
    subtitle = "Event study estimates: effect on log wages for college graduates",
    x = "Years Relative to Computer Adoption",
    y = "Effect on Log Wages",
    caption = "Simulated data illustrating event study design. Shaded area shows 95% CI."
  ) +
  theme_rhetoric()

ggsave("figures/fig3_event_study.pdf", p3, width = 10, height = 6.5)
ggsave("figures/fig3_event_study.png", p3, width = 10, height = 6.5, dpi = 300)

# =============================================================================
# Figure 4: Gender Wage Gap Over Time by Education
# =============================================================================

years3 <- seq(1960, 2020, 5)

# Female/Male earnings ratio (increasing over time)
wage_gap_data <- data.frame(
  year = rep(years3, 2),
  education = rep(c("College", "High School"), each = length(years3)),
  ratio = c(
    # College: starts lower, converges faster
    0.58 + 0.006 * (years3 - 1960) + 0.00005 * (years3 - 1960)^2 + rnorm(length(years3), 0, 0.015),
    # High School: starts higher, slower convergence
    0.62 + 0.004 * (years3 - 1960) + 0.00003 * (years3 - 1960)^2 + rnorm(length(years3), 0, 0.015)
  )
)

wage_gap_data$ratio <- pmin(wage_gap_data$ratio, 0.88)

p4 <- ggplot(wage_gap_data, aes(x = year, y = ratio, color = education, shape = education)) +
  # Reference line at parity
  geom_hline(yintercept = 1, linetype = "dashed", color = "#6C757D", linewidth = 0.5) +
  annotate("text", x = 1962, y = 0.98, label = "Parity", size = 3, color = "#6C757D", fontface = "italic") +
  # Data
  geom_line(linewidth = 1.1) +
  geom_point(size = 3) +
  # Direct labels
  annotate("text", x = 2022, y = 0.86, label = "College",
           color = "#2E4057", fontface = "bold", hjust = 0, size = 4) +
  annotate("text", x = 2022, y = 0.80, label = "High School",
           color = "#048A81", fontface = "bold", hjust = 0, size = 4) +
  scale_color_manual(values = c("College" = "#2E4057",
                                "High School" = "#048A81")) +
  scale_shape_manual(values = c("College" = 16, "High School" = 17)) +
  scale_x_continuous(breaks = seq(1960, 2020, 10), limits = c(1960, 2032)) +
  scale_y_continuous(labels = percent_format(accuracy = 1), limits = c(0.55, 1.02)) +
  labs(
    title = "The Narrowing Gender Wage Gap",
    subtitle = "Female-to-male earnings ratio among full-time workers",
    x = "Year",
    y = "Female/Male Earnings Ratio",
    caption = "Data patterns based on CPS ASEC. Full-time, year-round workers aged 25-54."
  ) +
  theme_rhetoric() +
  theme(legend.position = "none")

ggsave("figures/fig4_gender_gap.pdf", p4, width = 10, height = 6.5)
ggsave("figures/fig4_gender_gap.png", p4, width = 10, height = 6.5, dpi = 300)

# =============================================================================
# Figure 5: Skill Premium Decomposition (Supply vs Demand)
# =============================================================================

years4 <- 1965:2020

# Create supply and demand indices
supply_index <- numeric(length(years4))
demand_index <- numeric(length(years4))

for (i in seq_along(years4)) {
  yr <- years4[i]
  # Supply of college workers: steady increase
  supply_index[i] <- 100 + 2.5 * (yr - 1965) + rnorm(1, 0, 2)

  # Demand: accelerates after 1980
  if (yr <= 1980) {
    demand_index[i] <- 100 + 2.0 * (yr - 1965) + rnorm(1, 0, 2)
  } else {
    demand_index[i] <- 100 + 2.0 * 15 + 3.5 * (yr - 1980) + rnorm(1, 0, 2)
  }
}

df_supply_demand <- data.frame(
  year = rep(years4, 2),
  type = rep(c("Supply of College Workers", "Demand for College Workers"), each = length(years4)),
  index = c(supply_index, demand_index)
)

p5 <- ggplot(df_supply_demand, aes(x = year, y = index, color = type, linetype = type)) +
  # Annotation for divergence
  annotate("rect", xmin = 1980, xmax = 2020, ymin = -Inf, ymax = Inf,
           fill = "#E85D04", alpha = 0.05) +
  geom_line(linewidth = 1.2) +
  # Direct labels
  annotate("text", x = 2000, y = 260, label = "Demand\n(Accelerating)",
           color = "#E85D04", fontface = "bold", size = 3.8) +
  annotate("text", x = 2005, y = 200, label = "Supply\n(Steady)",
           color = "#048A81", fontface = "bold", size = 3.8) +
  annotate("text", x = 1990, y = 100, label = "SBTC Era:\nDemand outpaces supply",
           color = "#E85D04", fontface = "italic", size = 3.2) +
  scale_color_manual(values = c("Supply of College Workers" = "#048A81",
                                "Demand for College Workers" = "#E85D04")) +
  scale_linetype_manual(values = c("Supply of College Workers" = "solid",
                                   "Demand for College Workers" = "solid")) +
  scale_x_continuous(breaks = seq(1970, 2020, 10)) +
  scale_y_continuous(limits = c(90, 280)) +
  labs(
    title = "The Race Between Education and Technology",
    subtitle = "Index of relative supply and demand for college-educated workers (1965 = 100)",
    x = "Year",
    y = "Index (1965 = 100)",
    caption = "Conceptual illustration based on Goldin & Katz (2008) framework."
  ) +
  theme_rhetoric() +
  theme(legend.position = "none")

ggsave("figures/fig5_supply_demand.pdf", p5, width = 10, height = 6.5)
ggsave("figures/fig5_supply_demand.png", p5, width = 10, height = 6.5, dpi = 300)

# =============================================================================
# Figure 6: Bad vs Good Visualization Example (for the deck itself)
# This creates a "bad" cluttered chart as a teaching example
# =============================================================================

# Create sample data
bad_data <- data.frame(
  category = c("Q1", "Q2", "Q3", "Q4"),
  value2018 = c(45, 52, 48, 61),
  value2019 = c(48, 55, 51, 65),
  value2020 = c(43, 49, 47, 58),
  value2021 = c(52, 61, 55, 72),
  value2022 = c(58, 68, 62, 78)
)

# Bad version with default settings, 3D-like effects, etc.
bad_long <- bad_data %>%
  pivot_longer(cols = -category, names_to = "year", values_to = "value") %>%
  mutate(year = gsub("value", "", year))

p_bad <- ggplot(bad_long, aes(x = category, y = value, fill = year)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = c("2018" = "#FF0000", "2019" = "#00FF00",
                               "2020" = "#0000FF", "2021" = "#FFFF00", "2022" = "#FF00FF")) +
  labs(title = "QUARTERLY PERFORMANCE DATA 2018-2022",
       x = "QUARTER", y = "VALUE") +
  theme_gray() +
  theme(
    plot.title = element_text(size = 10, face = "bold"),
    legend.position = "right",
    panel.grid = element_line(color = "gray30"),
    axis.text = element_text(size = 8)
  )

ggsave("figures/fig6_bad_chart.pdf", p_bad, width = 8, height = 5)
ggsave("figures/fig6_bad_chart.png", p_bad, width = 8, height = 5, dpi = 300)

# Good version: focused, clean, direct labels
good_data <- data.frame(
  year = 2018:2022,
  q4_value = c(61, 65, 58, 72, 78)
)

p_good <- ggplot(good_data, aes(x = year, y = q4_value)) +
  geom_line(linewidth = 1.3, color = palette_main["primary"]) +
  geom_point(size = 4, color = palette_main["primary"]) +
  geom_point(data = good_data %>% filter(year == 2022),
             size = 5, color = palette_main["accent"]) +
  annotate("text", x = 2022.15, y = 78, label = "78",
           fontface = "bold", color = palette_main["accent"], hjust = 0, size = 5) +
  scale_x_continuous(breaks = 2018:2022) +
  scale_y_continuous(limits = c(50, 85)) +
  labs(
    title = "Q4 Performance: 28% Growth Over 5 Years",
    x = NULL,
    y = "Performance Index"
  ) +
  theme_rhetoric() +
  theme(panel.grid.major.x = element_blank())

ggsave("figures/fig6_good_chart.pdf", p_good, width = 8, height = 5)
ggsave("figures/fig6_good_chart.png", p_good, width = 8, height = 5, dpi = 300)

# =============================================================================
# Create regression output data for the deck
# =============================================================================

# Simulated regression results
reg_results <- data.frame(
  variable = c("College Degree", "Female", "College × Female",
               "Experience", "Experience²/100", "Urban", "Constant"),
  coef = c(0.482, -0.215, 0.067, 0.038, -0.065, 0.124, 1.847),
  se = c(0.023, 0.018, 0.031, 0.003, 0.008, 0.015, 0.042),
  stringsAsFactors = FALSE
)

reg_results$t_stat <- reg_results$coef / reg_results$se
reg_results$stars <- ifelse(abs(reg_results$t_stat) > 2.576, "***",
                            ifelse(abs(reg_results$t_stat) > 1.96, "**",
                                   ifelse(abs(reg_results$t_stat) > 1.645, "*", "")))

write.csv(reg_results, "figures/regression_results.csv", row.names = FALSE)

# =============================================================================
# Print completion message
# =============================================================================

cat("\n========================================\n")
cat("All figures generated successfully!\n")
cat("========================================\n")
cat("\nFiles created in figures/ directory:\n")
cat("  - fig1_college_premium.pdf/png\n")
cat("  - fig2_lfp_education.pdf/png\n")
cat("  - fig3_event_study.pdf/png\n")
cat("  - fig4_gender_gap.pdf/png\n")
cat("  - fig5_supply_demand.pdf/png\n")
cat("  - fig6_bad_chart.pdf/png\n")
cat("  - fig6_good_chart.pdf/png\n")
cat("  - regression_results.csv\n")
cat("\n")
