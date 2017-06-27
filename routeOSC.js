//outlets = 20;
/*
function routeMessage(label, incoming) {
  var [parsedIndex, parsedValue] = incoming.split(label)[1].split(' ');
  outlet(parsedIndex-1, parseFloat(parsedValue));
}
*/
function grid(label, rows, columns, incoming) {
  var [parsedIndex, parsedValue] = incoming.split(label)[1].split(' ');
  var row = ((parsedIndex-1)/rows)|0;
  var column = (parsedIndex-1)%columns
  outlet(0, [column, row, parseFloat(parsedValue)]);
}
