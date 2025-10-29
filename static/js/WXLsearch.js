$(document).ready(function(){ 
    //点提交按钮，发请求 
    $("#submit2index").on("click", function () { 
        $.ajax({ 
            type: "post", 
            url: "/buildindex", 
            data: {"id": $("#submit2index").attr("id")}, 
            dataType: "json", 
            beforeSend: function() { 
                // 设置 disabled 阻止用户继续点击 
                $("#submit2index").attr("disabled", "disabled"); 
            }, 
            complete: function () { 
                // 请求完成移除 disabled 属性 
                $("#submit2index").removeAttr("disabled"); 
            }, 
            success: function(result){ 
                if(result.status == 200){ 
                    console.log(result.text);  
                }else{ 
                    alert("索引失败"); 
                } 
            }, 
            error: function (jqXHR, textStatus, e) { 
                alert("提交异常："+e); 
            } 
        }); 
    });
    // 点击检索按钮，发请求 
    $("#chatbotsendbtn").on("click", function () { 
        var searchtext = $.trim($('#chattextarea').val()); 
        if (searchtext == "") { 
            alert("请输入您的问题"); 
            return; 
        } 

        // 将问题添加到聊天窗口的末尾 
        var question_html = '<div class="item item-right">' + '<div class="bubble bubble-right">' + searchtext + '</div>'  + '<div class="avatar avatar-user"></div>'  + '</div>'; 
        $('.content').append(question_html); 
        // 清空问题文本框  
        $('#chattextarea').val(''); 
        $('#chattextarea').focus(); 
        // 滚动条置底 
        var height = $('.content').scrollTop(); 
        $(".content").scrollTop(height); 
        
        $.ajax({ 
            type: "get", 
            url: "/searchanswer", 
            data: { 
                "id": $("#chatbotsendbtn").attr("id"), 
                "text": searchtext 
            }, 
            dataType: "json", 
            beforeSend: function() { 
                // 设置 disabled 阻止用户继续点击 
                $("#chatbotsendbtn").attr("disabled", "disabled"); 
            }, 
            complete: function () { 
                // 请求完成移除 disabled 属性 
                $("#chatbotsendbtn").removeAttr("disabled"); 
            }, 
            success: function(result){ 
                if(result.status == 200){ 
                    // 将基于问题理解回复的答案添加到聊天窗口的末尾 
                    var question_understanding_html = '<div class="item item-left">' + '<div class="avatar avatar-bot"></div>' + '<div class="bubble bubble-left">' + result.text + '</div>' + '</div>'; 
                    $('.content').append(question_understanding_html); 
                    // 滚动条置底 
                    var height = $('.content').scrollTop(); 
                    $(".content").scrollTop(height); 
                    console.log("问题理解回复成功"); 
                    
                    // 显示检索的其他答案
                    result.retrieval_answers.forEach(function(answer) {
                        var retrieval_answer_html = '<div class="item item-left">' + '<div class="avatar avatar-bot"></div>' + '<div class="bubble bubble-left">' + answer + '</div>' + '</div>';
                        $('.content').append(retrieval_answer_html); 
                        // 滚动条置底 
                        var height = $('.content').scrollTop(); 
                        $(".content").scrollTop(height); 
                    });

                    // 显示机器学习回复的答案
                    result.ml_answers.forEach(function(answer) {
                        var ml_answer_html = '<div class="item item-left">' + '<div class="avatar avatar-bot"></div>' + '<div class="bubble bubble-left">' + answer + '</div>' + '</div>';
                        $('.content').append(ml_answer_html); 
                        // 滚动条置底 
                        var height = $('.content').scrollTop(); 
                        $(".content").scrollTop(height); 
                    });

                    // 显示模型微调回复的答案
                    result.fine_tuned_answers.forEach(function(answer) {
                        var fine_tuned_answer_html = '<div class="item item-left">' + '<div class="avatar avatar-bot"></div>' + '<div class="bubble bubble-left">' + answer + '</div>' + '</div>';
                        $('.content').append(fine_tuned_answer_html); 
                        // 滚动条置底 
                        var height = $('.content').scrollTop(); 
                        $(".content").scrollTop(height); 
                    });
                } 
                else{ 
                    // 将答案添加到聊天窗口的末尾 
                    var no_answer_html = '<div class="item item-left">' + '<div class="avatar avatar-bot"></div>' + '<div class="bubble bubble-left">对不起！我不明白您的问题，可以换种问法吗？</div>' + '</div>'; 
                    $('.content').append(no_answer_html); 
                    // 滚动条置底 
                    var height = $('.content').scrollTop(); 
                    $(".content").scrollTop(height); 
                    console.log("检索不到答案"); 
                }  
            }, 
            error: function (jqXHR, textStatus, e) { 
                alert("提交异常："+e); 
            } 
        }); 
    });
    $("#imageUploadBtn").on("click", function() {
        $("#imageUpload").click(); // 点击按钮触发文件选择对话框
    });

    $("#imageUpload").on("change", function() {
        var file = this.files[0]; // 获取选择的文件
        if (file) {
            var reader = new FileReader(); // 创建一个文件读取对象
            reader.onload = function(e) {
                var imageUrl = e.target.result; // 获取图片的 Base64 编码
                // 在前端页面中显示图片
                var image_html = '<div class="item item-right">' +
                                    '<div class="avatar avatar-user"></div>' +
                                    '<div class="bubble bubble-right"><img class="uploaded-image" src="' + imageUrl + '"></div>' +
                                  '</div>';
                $('.content').append(image_html);
                // 滚动条置底 
                var height = $('.content').scrollTop(); 
                $(".content").scrollTop(height); 
            };
            reader.readAsDataURL(file); // 读取文件
        }
    });
    $("#audioUploadBtn").on("click", function() {
        // 触发文件选择对话框
        $("#audioUpload").click();
    });

    $("#audioUpload").on("change", function() {
        var file = this.files[0]; // 获取选择的文件
        if (file) {
            uploadAudio(file); // 调用上传函数
        }
    });

    function uploadAudio(file) {
        var formData = new FormData();
        formData.append("audioFile", file);

        $.ajax({
            type: "POST",
            url: "/upload_audio", // 这里填写服务器端接收音频文件的URL
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log("音频上传成功");
                // 这里可以根据服务器的响应做一些操作，比如在聊天窗口中显示已上传的音频文件
            },
            error: function(xhr, status, error) {
                console.error("音频上传失败:", error);
            }
        });
    }
})