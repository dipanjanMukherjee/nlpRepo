
#library part left

df_orig <- read.csv("topics.csv", stringsAsFactors = F)


#eliminate rows with all columns as NA
df_change <- df_orig[rowSums(is.na(df_orig)) != ncol(df_orig),]
df_null <- df_orig[is.na(df_orig$AlertName),]
df_orig <- df_orig[!is.na(df$AlertName),]
df_dupl <- df_orig
df <- df_dupl

corpus <- Corpus(VectorSource(df),readerControl = list(blank.lines.skip = TRUE))
dtm <- DocumentTermMatrix(corpus)
dtm_m <- as.matrix(dtm)
tdm_m <- as.matrix(t(dtm))

#convert tdm to a list of texxtt
dtm2list <- apply(dtm,1,function(x){
  paste(rep(names(x),x),collapse = "")
})

#convert to a corpus
corpus <- VCorpus(VectorSourcce(dtm2list))
corpus <- tm_map(corpus,toSpace,"-")
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, stemDocument,"english")

skipstopwords <- function(x) removeWords(x,stopwords("english"))
corpus <- tm_map(corpus, skipstopwords)

#create dtm post cleaning
dtm <- DocumentTermMatrix(corpus)
dtm <- removeSparseTerms(dtm, sparse = 0.999)
dtm_ma <- as.matrix(dtm)
tdm_ma <- as.matrix((t(dtm)))
                    
#word frequency
wf <- wordFreqGeneration()
p <- ggplot(subset(wf, freq > input$freqSlider), aes(x = reorder(word,freq), y= freq))
p <- p+ geom_bar(stat="identity",fill="blue",col="blue")
p <- p + theme(axis.text.x=element_text(angle=45, hjust=1))
p <- p + coord_flip()
p <- p + ggtitle("Term Frequency Plot") + xlab("Frequency") + ylab("Term")
p
                    
#wordcloud
dtm_m <- read.csv(wordCloudFile$datapath)
dtm_m <- dtm_m[,-1]
freq <- colSums(dtm_m)
freq <- sort(freq, decreasing =TRUE)
set.seed(20)
wordcloud(names(freq), freq, min.freq = input$wordCloudSlider, colors = brewer.pal(6,"Dark2"))
                    
#correlation
freqTerms <- findFreqTerms(dtm, lowfreq = input$heatMapSlider)
c < - as.vector(freqTerms)
assocs <- as.matrix(findAssocs(dtm, c, input$corrFreqSlider))
assoc_v <- c("")
assoc_v_read <- c("")
for(i in 1:length(assocs)){
    for(j in 1:length(assocs[[i]])){
        assocs_v_read <- c(assoc_v, names(asssocs[[i]][[j]]))
     }
}
                    
assoc_v_read <- assoc_v_read[!is.na(assoc_v)]
                    
allTerms <- as.vector(dtm$dimname$Terms)
corTerms <- as.vector(assoc_v_read)
retainTerms <- unique(c(corTerms, freqTerms))
dtm_hm <- dtm[,(dtm$dimname$Terms) %in% retainTerms]
dtm_m <- as.matrix(dtm_hm)
                    
cor_hm <- cor(dtm_m)
cor_hm
                    
heatmap.2(
  as.matrix(cor_hm)
  , dendogram = 'none'
  , na.rm = TRUE
  , trace = 'none'
  , col = colorRampPalette(c("white","orange"))(256)
  , density.info = 'none')
                    
#
all_zero_rows <- as.vector(rowSums(dtm_m))
isZero <- function(X) { if (X==0) return (TRUE) else return(FALSE) }
z_rows <- Filter(isZero,all_zero_rows)
length(z_rows)
rowTotals <- apply(dtm,1,sum)
dtm_new <- dtm[rowTtoals >0, ]
dtm_new
                    
non_relevant <- as.vector(which(rowTotals == 0))
unclustered_tickets <- filter(df, rownames(df) %in% non_relevant)
unclustered_tickets <- unclustered_ticekts[,-1]
unclustered_tickets
                    
                    
                    