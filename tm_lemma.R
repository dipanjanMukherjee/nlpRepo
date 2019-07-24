#library part left

dtm_m <- as.matrix(dtm)

coln <- colnames(dtm_m)
lemmatized_terms <- lemmatize_words(coln)
colnames(dtm_m) <- lemmatized_terms

#merging columns with same column name, ?
dtm_m %*% sapply(unique(lemmatized_terms),"==", lemmatized_terms)

dtm_m


### ?
sk_cum <- c("")
temp <- 0
for(i in 1:length(LSAspace$sk)){
  temp <- temp + ((LSAspace$sk[i]^2/sum(LSAspace$sk^2))*10)
  sk_cum <- c(sk_cum, round(temp,2))
}

sk_cum <- sk_cum[-1]
sk_cum <- as.matrix(sk_cum)
colnames <- sk_cum <- c("Variance")

num_cluster <- length(LSAspace$sk)

sk_cum