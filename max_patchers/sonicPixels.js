outlets = 8;

function hexlify(row, input) {
	var theNumber = parseInt(input, 2);
	var theHex = theNumber.toString(16);
	while (theHex.length < 2) {
		theHex = "0" + theHex;
	}
	outlet(row, theHex);
}
