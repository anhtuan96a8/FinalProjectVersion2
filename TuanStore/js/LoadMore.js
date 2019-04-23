function LoadMorePro(skipnum,action,id,id1) {
    var url = "/Home/"+action;
    $.ajax({
        url: url,
        type: 'Get',
        data: {skip:skipnum},
        success: function (result) {
            var a = result.toString();
            if (!a)
            {
                $(id).html(a);
            }
            else
            {
                $(id1).append(result);
                skipnum += 4;
                var fixa = "<a class=\"btn-loadmore btn\" style=\"padding: 8px 22px 8px 22px;margin:70px 0 0 0; border-radius: 50px; background-color: #34495E; color: white; font-weight: bold\" href=\'javascript:LoadMorePro(" + skipnum.toString() + ",\"" + action + "\",\"" + id + "\",\"" + id1 + "\")\'>";
                fixa += "<i class=\"fa fa-plus\"></i>Tải thêm</a>";
                $(id).html(fixa);
            }
        },
    });
}