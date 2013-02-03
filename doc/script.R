## One Year
whip12 <- read.csv("2012_55108.csv", header=TRUE)
yield <- c(as.matrix(whip12[2:9])) # ignore the first column
Varieties <- factor(rep(c(as.matrix(whip12[1])), 8)) # extract the first column as a factor
Environments <- factor(rep(names(whip12)[2:9],rep(29, 8))) # extract the column headers as factors

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
Varieties <- factor(rep(c(as.matrix(whip12_11[1])), 4))
Environments <- factor(rep(names(whip12_11)[2:5], rep(46, 4)))

model <- aov(yield ~ Varieties + Environments)
mse <- deviance(model) / df.residual(model) 
require(agricolae)
LSD.test(yield, Varieties, df.residual(model), mse, alpha=0.05)
# LSD is 6.516289
qt(1-.05/2, df.residual(model)) * sqrt(2.0 * mse / 4)
# returns 9.215424, which is the source of the incorrect value WHIP is using.
