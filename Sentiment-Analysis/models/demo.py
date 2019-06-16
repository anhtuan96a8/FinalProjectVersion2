from train import predict_comments

if __name__ == '__main__':
    cmts = ["dong ho đep ,re,chay rat ngon cam on shop vs lazada.",
            "Thất vọng",
            "Sản phẩm rất hay bị rơi và văng khỏi dây đeo cao su. Độ sáng màn hình hơi thấp, nên ra ngoài đường hơi khó nhìn.",
            "Sản phẩm dùng cũng ok phết, trong tầm giá này thì con này dùng cũng tạm được",
            "Đẹp dã man, màn hình nhìn đã mắt, pin cực trâu, dùng mấy ngày mới hết",
            "gói không cẩn thận. không có hộp và pin dự phòng tặng kèm",
            "Quá tệ, không thể chấp nhận",
            "mới mua mà bị vô nước, máy ko chạy",
            "sản phẩm đẹp trên cả tuyệt vời .ok",
            "cho 3 sao",
            "quá chán",
            "cho 1 sao",
            "cho 4 sao",
            " cho 5 sao",
            "đồng hồ thì cũ , giao hàng thì chậm",
            "phí tiền",
            "chạy được 1 ngày thì sai 10p"
            ]
    predict_comments(cmts)
