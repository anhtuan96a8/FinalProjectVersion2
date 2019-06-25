# Web Bán Đồng Hồ áp dụng gợi ý thang điểm đánh giá và trả lời tự động ( còn có lọc đánh giá tự động )
# Download project and open it with Visual studio 
# Need : 
  + MS Sql Server 2012 Express LocalDB
  + Python 3.6
  + gensim , tensorflow, pyvi, numpy, flask, keras, .... ( cứ chạy thiếu cái gì thì install cái đó )
# Chạy Project :
  + Chạy file server.py trong folder Server
  + Chạy project web trên visual studio
  + Training lại file weight cho chatbot và sentiment analysis ở 2 folder cùng tên.
# Traning Chatbot 
  + Chạy word2vec để tạo từ điển
  + Chạy split_qa.py để tách question answer
  + Chạy get_train_data.py để tạo file word to index 
  + Chạy train_bot.py để training weight bot
# Traning Sentiment Analysis and Classifier
  + Chạy word2vec để tạo từ điển
  + Chạy Train.py để training Sentiment Analysis hoặc classifier
  + Chú ý : nhớ thay đổi pathModelBin ( thay đổi ở dòng 14 15 ) và thay đổi train sentiment hay classifier ( ở 2 dòng cuối)
