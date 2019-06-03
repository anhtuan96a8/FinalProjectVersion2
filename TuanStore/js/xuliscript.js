
    function Addcart(value, sl) {
        if (sl == 0) {
            alert("Xác nhận");
            sl = $('.sl').val();
        }
        var url = "/Xuligiohang/Addcart";
        $.ajax({
            url: url,
            type: 'Get',
            cache: false,
            data: { sp: value, quantity: sl },
            success: function (result) {
                $('.basket').html(result);
                alert("Thêm thành công");
            },
            error: function (result) {
                alert("Sản phẩm đã hết hàng");
            }
        });
    }

    function Huydonhang(value) {
        var url = "/Home/Huydonhang";
        $.ajax({
            url: url,
            type: 'Get',
            cache: false,
            data: { maDH: value },
            success: function (result) {
                $('.simpleCart_items').html(result);
            }
        });
    }
    // Cart
    function xoagiohang(value) {
        var url = "/Xuligiohang/Xoagiohang";
        $.ajax({
            url: url,
            type: 'Get',
            cache: false,
            data: { index: value },
            success: function (result) {
                $('#cart-page').html(result.toString());
                updatecontentCart();
            }
        });
    }
    function changequality(value, tt) {

        var id = "quantity+" + value;
        temp = document.getElementById(id).value;
        if (temp > 1 && tt == 'G')
            temp--;
        if (tt == 'T')
            temp++;
        var url = "/Xuligiohang/Thaydoisoluong";
        $.ajax({
            url: url,
            type: 'Get',
            cache: false,
            data: { index: value, value: temp },
            success: function (result) {
                $('#cart-page').html(result.toString());
                updatecontentCart();
            }
        });
    }
    function updatecontentCart() {
        var url = "/Xuligiohang/UpdategiohangContent";
        $.ajax({
            url: url,
            type: 'Get',
            cache: false,
            success: function (result) {
                $('.basket').html(result);
            }
        });
    }
    
   
