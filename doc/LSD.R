tapply.stat <-
function (y, x, stat = "mean") 
{
		cx <- deparse(substitute(x))
		cy <- deparse(substitute(y))
		x <- data.frame(c1 = 1, x)
		y <- data.frame(v1 = 1, y)
		nx <- ncol(x)
		ny <- ncol(y)
		namex <- names(x)
		namey <- names(y)
		if (nx == 2) 
				namex <- c("c1", cx)
		if (ny == 2) 
				namey <- c("v1", cy)
		namexy <- c(namex, namey)
		for (i in 1:nx) 
		{
				x[, i] <- as.character(x[, i])
		}
		z <- NULL
		for (i in 1:nx) 
		{
				z <- paste(z, x[, i], sep = "&")
		}
		w <- NULL
		for (i in 1:ny) 
		{
				m <- tapply(y[, i], z, stat)
				m <- as.matrix(m)
				w <- cbind(w, m)
		}
		nw <- nrow(w)
		c <- rownames(w)
		v <- rep("", nw * nx)
		dim(v) <- c(nw, nx)
		for (i in 1:nw) 
		{
				for (j in 1:nx) 
				{
						v[i, j] <- strsplit(c[i], "&")[[1]][j + 1]
				}
		}
		rownames(w) <- NULL
		junto <- data.frame(v[, -1], w)
		junto <- junto[, -nx]
		names(junto) <- namexy[c(-1, -(nx + 1))]
		return(junto)
}

t.quantile <- 
	function(probability, degreesfreedom)
{
	n <- degreesfreedom
	P <- probability
	t <- 0
	if (n < 1 || P > 1.0 || P <= 0.0 )
	{
		print(c("error"))
	}
	else if (n == 2)
	{
		t <- sqrt(2.0/(P*(2.0-P)) - 2.0)
	}
	else if (n == 1)
	{
		P <- P * pi/2
		t <- cos(P)/sin(P)
	}
	else
	{
		a <- 1.0/(n-0.5)
		b <- 48.0/(a^2)
		c <- ((20700*a/b - 98)*a - 16)*a + 96.36
		d <- ((94.5/(b+c) - 3.0)/b + 1.0)*sqrt(a*pi/2)*n
		x <- d*P
		y <- x^(2.0/n)
		
		if (y > 0.05 + a)
		{
			x <- qnorm(P*0.5)
			y <- x^2
			
			if (n < 5)
			{
				c <- c + 0.3*(n-4.5)*(x+0.6)
			}
			c <- (((0.05*d*x-5.0)*x-7.0)*x-2.0)*x+b+c
			y <- (((((0.4*y+6.3)*y+36.0)*y+94.5)/c-y-3.0)/b+1.0)*x
			y <- a*y^2
			
			if (y > 0.002)
			{
				y <- exp(y) - 1.0
			}
			else
			{
				y <- 0.5*y^2 + y
			}
		}
		else
		{
			y <- ((1.0/(((n+6.0)/(n*y)-0.089*d-0.822)*(n+2.0)*3.0)+0.5/(n+4.0))*y-1.0)*(n+1.0)/(n+2.0)+1.0/y
		}
		
		t <- sqrt(n*y)
	}
	
	return(t)
}

LSD.return <-
function (y, trt, DFerror, MSerror, alpha = 0.05, p.adj = c("none", 
		"holm", "hochberg", "bonferroni", "BH", "BY", "fdr"), group = TRUE, 
		main = NULL) 
{
	LSD <- c(NA)
	# Sets p.adj to "none" if no choice given in the function call
	#p.adj <- match.arg(p.adj)
	# Combine y/trt 1D-vectors into a 2D matrix w/ meta information, discarding nulls
	junto <- subset(data.frame(y, trt), is.na(y) == FALSE)
	# Calculate the mean of the y vector (junto[, 1]), and the trt vector (junto[, 2])
	#means <- tapply.stat(junto[, 1], junto[, 2], stat = "mean")
	# Calculate the standard deviation of y and trt
	#sds <- tapply.stat(junto[, 1], junto[, 2], stat = "sd")
	# Calculate the length of the y vectors
	# ...Unsure what the value for the trt vector signifies
	nn <- tapply.stat(junto[, 1], junto[, 2], stat = "length")
	# print(c("matrices",junto,"means",means,"standard deviations",sds,"lengths",nn))
	
	# Calculates the sd/sqrt(n) for each trt factor
	#std.err <- sds[, 2]/sqrt(nn[, 2])
	#print(c("std.err",std.err,"sds", sds[,2],"nn", nn[,2]))
	
	# Calculates the quantile function of the t-distribution using the p-significance and the degrees of freedom given
	Tprob <- qt(1 - alpha/2, DFerror)
	
	#print(c("t oracle", Tprob))
	#print(c("t", t.quantile(alpha, DFerror)))
	
	
	# Checks the length of the treatment groups.
	# i.e. unique(c(3,3,3,4)) -> c(3,4)
	nr <- unique(nn[, 2])

	print(c("nr", nr))
	# if all treatments had the same number of observations
	if (length(nr) == 1) 
	{
			LSD <- Tprob * sqrt(2 * MSerror/nr)

	}
	else 
	{
			nr1 <- 1/mean(1/nn[, 2])
			LSD1 <- Tprob * sqrt(2 * MSerror/nr1)
	}
	
	return(LSD)
}


y <- c(1,1,1,3,3,3,1,1,1,2,2,2)
trt <- factor(c(1,2,3,1,2,3,1,2,3,1,2,3), labels=c('a','b','c'))
# Apply lm() to each factor
model <- aov(y~trt)
# Grab the residual degrees of freedom from the 'model'
df <- df.residual(model)
print(c("df", df))
# Calaculate the Mean Squares by dividing the deviance of the 'model' and dividing it by the degrees of freedom
MS <- deviance(model) / df
print(c("MS", MS))
print(c("oracle:",1.531488))
LSD.return(y, trt, df, MS)
require(agricolae)
LSD.test(y,trt,df,MS)

