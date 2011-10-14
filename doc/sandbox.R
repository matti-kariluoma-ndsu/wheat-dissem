
barnes <-		c(90.5,	86.9,	89.9,	96.9,	85.4,	86.3,	83.8,	92.7)
crookston <-	c(73.1,	78.4,	78.0,	92.1,	84.7,	90.2,	77.6,	71.4)
dickey <-		c(61.7,	76.9,	56.4,	61.1,	56.3,	69.6,	67.2,	62.0)
fergus <-		c(81.5,	72.1,	71.7,	96.8,	84.3,	85.0,	84.2,	82.1)
nelson <-		c(76.8,	69.1,	74.5,	82.9,	78.2,	69.1,	70.2,	63.0)
oklee <-		c(78.0,	99.8,	83.1,	105.6,77.4,	110.2,94.3,	81.0)
perley <-		c(70.3,	62.3,	68.1,	75.6,	74.5,	67.7,	75.3,	72.3)

# treatment <- c(barnes, crookston, dickey, fergus, nelson, oklee, perley)

alpha <- 0.05

n <- 7 # length(treatment) number of locations
k <- 8 # length(barnes)
degrees_freedom_of_error <- (n-1)*(k-1)

squared_sums_of_error <- 0.0
squared_sums_of_error <- squared_sums_of_error + sum((mean(barnes) - barnes)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(crookston) - crookston)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(dickey) - dickey)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(fergus) - fergus)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(nelson) - nelson)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(oklee) - oklee)^2)
squared_sums_of_error <- squared_sums_of_error + sum((mean(perley) - perley)^2)


mean_squares_of_error <- squared_sums_of_error / degrees_freedom_of_error

LSD <- qt(1 - alpha/2, degrees_freedom_of_error) * sqrt(2.0 * mean_squares_of_error / k)

print(LSD)
