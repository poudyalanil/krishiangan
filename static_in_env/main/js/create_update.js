$('form').find('input,  select, textarea,number').each(function () {
    
    if($(this).attr('type') !== 'checkbox'){
        $(this).addClass('form-control');
    }

    if($(this).attr('rows') !== 'undefined'){
        // $(this).attr('rows',4);
    }

    if($(this).attr('col')){
        if($(this).attr('type') == 'checkbox'){
            if($(this).attr('col-parent')){
                $(this).parent().parent().parent().parent().addClass($(this).attr('col'));
            }else{
                $(this).parent().parent().parent().addClass($(this).attr('col'));
                $(this).parent().addClass('pt-5 pl-3 font-weight-bold');
            }
        }else{
            $(this).parent().parent().parent().addClass($(this).attr('col'));
        }
    }

});



