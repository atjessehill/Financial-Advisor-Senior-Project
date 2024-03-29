//Actually this needs to be an IIFE
(function (global) {

    //fake namespace to expose it
    let autoObject = {};
    //Holy shit this is the answer to the project I am a fucking genius.

    autoObject.names = $nameObj.peopleNames;
    autoObject.countries = $nameObj.countryNames;


    autoObject.autocomplete = function (inp, arr) {

        /*the autocomplete function takes two arguments,
        the text field element and an array of possible autocompleted                   values:*/
        let currentFocus;
        /*execute a function when someone writes in the text field:*/
        inp.addEventListener("input", function (e) {
            let maxDisplays = 5;
            let count = 0;
            let a, b, i, val = this.value;
            /*close any already open lists of autocompleted values*/
            closeAllLists();
            if (!val) {
                return false;
            }
            currentFocus = -1;
            /*create a DIV element that will contain the items (values):*/
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items");
            /*append the DIV element as a child of the autocomplete container:*/
            this.parentNode.appendChild(a);
            /*for each item in the array, this seems to be the shitload...fixing this*/
            for (i = 0; i < arr.length; i++) {
                //init number of autocompletes. Can change global above to increase
                    /*check if the item starts with the same letters as the text field value:*/
                    if (count < maxDisplays && arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                        count++;
                        /*create a DIV element for each matching element:*/
                        b = document.createElement("DIV");
                        /*make the matching letters bold:*/
                        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                        b.innerHTML += arr[i].substr(val.length);
                        /*insert a input field that will hold the current array item's value:*/
                        b.innerHTML += "<input  type='hidden' value='" + arr[i] + "'>";
                        /*execute a function when someone clicks on the item value (DIV element):*/
                        b.addEventListener("click", function (e) {
                            /*insert the value for the autocomplete text field:*/
                            inp.value = this.getElementsByTagName("input")[0].value;
                            /*close the list of autocompleted values,
                            (or any other open lists of autocompleted values:*/
                            closeAllLists();
                        });
                        a.appendChild(b);
                    }
                }

        });
        /*execute a function presses a key on the keyboard:
        * deprecated.. find out how to fix this*/
        inp.addEventListener("keydown", function (e) {
            let x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            console.log(x);
            if (e.which == 40) {
                /*increment the target in our array, and we will color this*/
                currentFocus++;
                /*use currentFocus to highlight current div*/
                console.log(x[currentFocus]);

                addActive(x);
            } else if (e.which == 38) { //up
                /*increment the target in our array, and we will color this*/
                currentFocus--;
                /*and and make the current item more visible:*/
                addActive(x);
            } else if (e.which == 13) {
                /*If the ENTER key is pressed, prevent the form from being submitted,*/
                e.preventDefault();
                if (currentFocus > -1) {
                    /*and simulate a click on the "active" item:*/
                    if (x) x[currentFocus].click();
                }
            }
        });

        function addActive(x) {
            /*a function to classify an item as "active":*/
            if (!x) return false;
            /*start by removing the "active" class on all items:*/
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = (x.length - 1);
            /*add class "autocomplete-active":*/
            x[currentFocus].classList.add("autocomplete-active");
        }


        function removeActive(x) {
            /*a function to remove the "active" class from all autocomplete items:*/
            for (let i = 0; i < x.length; i++) {
                x[i].classList.remove("autocomplete-active");
            }
        }

        function closeAllLists(elmnt) {
            /*close all autocomplete lists in the document,
            except the one passed as an argument:*/
            let x = document.getElementsByClassName("autocomplete-items");
            for (let i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }

        /*execute a function when someone clicks in the document:*/
        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
    }
    //expose object so we can call autocomplete function in dynamic separate HTML
    global.$autoObject = autoObject;

})(window);
