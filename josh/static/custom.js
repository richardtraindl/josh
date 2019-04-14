

    function showPromotion(){
        var fieldid = $('#move-src').val();
        var piece = $('#' + fieldid).attr("value");
        if( piece == 'wPw' ){
            var row = $('#move-dst').val();
            if( row.charAt(1) == '8' ){
                $('#white-pieces').removeClass("invisible");
                $('#prom-piece').removeAttr("readonly");
                return true;
            }
        }
        else if( piece == 'bPw' ){
            var row = $('#move-dst').val();
            if( row.charAt(1) == '1' ){
                $('#black-pieces').removeClass("invisible");
                $('#prom-piece').removeAttr("readonly");
                return true;
            }
        }

        return false;
    }

    function performMove(){
        $('#board > div').click(function(){
            if( $(this).hasClass("marked") ){
                $(this).removeClass("marked");
                $('#white-pieces').addClass("invisible");
                $('#black-pieces').addClass("invisible");
                $('#prom-piece').attr("readonly", "readonly");
                if( $('#move-dst').val().trim() == $(this).attr("id") ){
                    $('#move-dst').val("");
                }
                else if( $('#move-src').val().trim() == $(this).attr("id") ){
                    $('#move-src').val("");
                    $('#move-dst').val("");
                }
            }
            else{
                $(this).addClass("marked");
                var src = $('#move-src').val();
                if(! src.trim() ){
                    $('#move-src').val($(this).attr("id"));
                }
                else{
                    $('#move-dst').val($(this).attr("id"));
                    if(showPromotion() == false){
                        $("#move").submit();
                    }
                }
            }
        });
    }
    
    
    function drag() {
        $('.draggable').draggable({
          start: function( event, ui ){
            var src = $(this).parent().attr("id");
            $('#move-src').val( src );
          }
        });
    }

    function drop() {
        $('.droppable').droppable({
          drop: function( event, ui ) { 
              var dst1 = $(this).attr("id");
              $('#move-dst').val( dst1 );

              var src1 = $('#move-src').val();
              if( src1.trim() == dst1.trim() ){
                $('#move-src').val("");
                $('#move-dst').val("");
              }else{
                if(showPromotion() == false){
                    $("#move").submit(); 
                }
              }
          }
        });
    }
