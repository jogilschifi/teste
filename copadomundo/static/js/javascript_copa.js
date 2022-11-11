(function (win,doc){
    "use strict";

})(window,document);

  var visibleDiv = 0;
  function showDiv()
  {
    $(".grid").hide();
    $(".grid:eq("+ visibleDiv +")").show();
  }
  showDiv()

function showNext()
{
  if(visibleDiv== $(".grid").length-1)
  {
    visibleDiv = 0;
  }
  else {
    visibleDiv ++;
  }
  showDiv();
}


function showPrev()
{
  if (visibleDiv == 0)
  {
    visibleDiv= $(".grid").length-1
  }
  else {
    visibleDiv --;
  }
  showDiv();
}