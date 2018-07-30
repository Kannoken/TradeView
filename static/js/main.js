$(document).ready(function () {
var $li = $('li').click(function() {
    $li.removeClass('selected');
    $(this).addClass('selected');
});
    $('li').click(function () {
        $.post('/', {id : this.id}).done(function (result) {
            let $marq =$('#marq').detach();
            let str = '';
            for (let key in result.result){
                str+=' date: '+key+' abs: '+result.result[key].abs + ' close: '+result.result[key].close + ' '+ result.result[key].per
            }
            $marq.innerHTML = str;
            $marq.appendTo('body')

        })
    })
});
