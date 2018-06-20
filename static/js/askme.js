$(document).ready( () => {
  $('.minus-button').click( (e) => {
    const currentInput = $(e.currentTarget).parent().next().children()[0];
    let minusInputValue = $(currentInput).html();
      minusInputValue --;
      $(currentInput).html(minusInputValue);
  });

  $('.plus-button').click( (e) => {
    const currentInput = $(e.currentTarget).parent().prev().children()[0];
    let plusInputValue = $(currentInput).html();
    plusInputValue ++;
    $(currentInput).html(plusInputValue);
  });
});