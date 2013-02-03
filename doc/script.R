whip12 <- read.csv("2012_55108.csv", header=TRUE)
whip11 <- read.csv("2011_55108.csv", header=TRUE)
whip10 <- read.csv("2010_55108.csv", header=TRUE)


## One Year
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

## Two Years
yield <- 

is.na(whip11[,2][1])
names(whip11)