## One Year
whip12 <- read.csv("2012_55108.csv", header=TRUE)
yield <- c(as.matrix(whip12[2:9])) # ignore the first column
Environments <- factor(rep(names(whip12)[2:9],rep(29, 8))) # extract the column headers as factors
Varieties <- factor(rep(c(as.matrix(whip12[1])), 8)) # extract the first column as a factor

model <- aov(yield ~ Varieties + Environments)
mse <- deviance(model) / df.residual(model) 
require(agricolae)
LSD.test(yield, Varieties, df.residual(model), mse, alpha=0.05)
# LSD is 4.603553
# which is equivalent (?) to
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 8) # 8 Observations of each variety
# returns 4.603553

## Two Years
whip12_11 <- read.csv("2012-2011_55108.csv", header=TRUE)
yield <- c(as.matrix(whip12_11[2:5]))
Environments <- factor(rep(names(whip12_11)[2:5], rep(46, 4)))
Varieties <- factor(rep(c(as.matrix(whip12_11[1])), 4))

model <- aov(yield ~ Varieties + Environments)
mse <- deviance(model) / df.residual(model) 
require(agricolae)
LSD.test(yield, Varieties, df.residual(model), mse, alpha=0.05)
# LSD is 6.516289
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 4)
# returns 9.215424, which is the source of the incorrect value WHIP is using.
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 8)
# returns 6.516289

## Two years, unbalanced
un_whip12_11 <- read.csv("Unbalanced_2012-2011_55108.csv", header=TRUE)

yield <- c(as.matrix(un_whip12_11[2:17]))
Environments <- factor(rep(names(un_whip12_11)[2:9], rep(29*2,8)))
Varieties <- factor(rep(c(as.matrix(un_whip12_11[1])), 16))

model <- aov(yield ~ Varieties + Environments)
mse <- deviance(model) / df.residual(model) 
require(agricolae)
LSD.test(yield, Varieties, df.residual(model), mse, alpha=0.05)
# LSD is 11.70167
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 16)
# returns 9.647224, incorrect
avg_observations <- (1 - length(Filter(is.na, yield)) / length(yield)) * 16
# simple average is 11.17 observations per variety
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / avg_observations)
# returns 11.54487, incorrect
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 10.87499)
# returns 11.70167, correct, but 10.8 observations per variety...?
