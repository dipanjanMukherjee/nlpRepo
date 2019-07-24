## library part left


corpus <- Corpus(VectorSource(df$`desc`), readerControl = list(blank.lines.skip = TRUE))
toSpace <- content_transformer(function(x, pattern) {return (gsub(pattern, x))})

corpus <- tm_map(corpus, toSpace, "-")
corpus <- tm_map(corpus, toSpace, "'")
corpus <- tm_map(corpus, toSpace, "/")
corpus <- tm_map(corpus, toSpace, "?")
corpus <- tm_map(corpus, toSpace, ".")
corpus <- tm_map(corpus, toSpace, ";")
corpus <- tm_map(corpus, toSpace, "@")
corpus <- tm_map(corpus, toSpace, "\ ")
corpus <- tm_map(corpus, toSpace, "%")

corpus <- tm_map(corpus, removePunctuation)

corpus <- tm_map(corpus, content_transformer(tolower))

corpus <- tm_map(corpus, stripWhitespace)

skipStopWords <- function(x) removeWords(x, stopwords("english"))

corpus <- tm_map(corpus, skipStopWords)

dtm <- DocumentTermMatrix(corpus)

dtm <- removeSparseTerms(dtm, sparse = 0.999)

dtm_m <- as.matrix(dtm)

custom_stopwrds <- read.csv("stopwords.csv")

custom_stop <- c(custom_stopwrds$stopwords)

skipContextWords <- function(x) removeWords(x, custom_stop)

corpus <- tm_map(corpus, skipContextWords)

BiGramTokenizer <- function(x) NGramTokenizer(x, Weka_control(min = 1, max = 2))

dtm <- DocumentTermMatrix(corpus, control = list(tokenize = BiGramTokenizer, wordLength = 10))

dtm <- removeSparseTerms(dtm, sparse = 0.999)

#remove docuemnts that does not contain any words
rowTotals <- apply(dtm, 1, sum)
dtm.new <- dtm[rowTotals > 0,]
rownames(dtm.new) <- 1:nrow(dtm.new)

non_relevant <- as.vector(which(rowTotals == 0))
unclustered_tickets <- filter(df1, rownames(df1) %in% non_relevant)
dim(unclustered_tickets)

df_new <- filter(df1, !row.number() %in% non_relevant)

write.csv(unclustered_tickets, "unclustered1.csv")

#normalize dtm
dtm_tfidf <- weightTfIdf(dtm.new)
dtm_tfidf_m <- as.matrix(dtm_tfidf)
rownames(dtm_tfidf_m) <- 1:nrow(dtm_tfidf_m)

#euclidian form of dtm ?
norm_eucl <- function(m) m/apply(m, MARGIN = 1, FUN = function(x) sum(x^2)^0.5)
dtm_tfidf_m_norm <- norm_eucl(dtm_tfidf_m)

library(lsa)
library(LSAfun)

dtm_scale <- scale(dtm_tfidf)

LSASpace <- lsa(t(dtm_scale), dims = dimcalc_raw())

print("dimension of document term matrix of lsa space is:")
dim(LSASpace$tk)
dim(LSASpace$dk)
length(LSASpace$sk)

num_cluster <- length(LSASpace$sk)
set.seed(4)
fit.km <- kmeans(dtm_tfidf_m_norm, num_cluster, nstart = 18)
round(fit.km$centers, digits = 1)

kmeans_cluster <- cbind(df_new, fit.km$cluster)

