var __PDF_DOC,
  __CURRENT_PAGE,
  __TOTAL_PAGES,
  __PAGE_RENDERING_IN_PROGRESS = 0,
  TEXT_LAYER_HAS_RENDERED = false,
  __CANVAS = $("#pdf-canvas").get(0),
  __CANVAS_CTX = __CANVAS.getContext("2d");

//function to determine where to place the tooltip
function determine(event) {
  const vw = Math.floor(
    Math.max(document.documentElement.clientWidth, window.innerWidth || 0) / 2
  );
  const position = event.clientX;
  if (position > vw) {
    return "left";
  } else if (position == vw) {
    return "top";
  } else {
    return "right";
  }
}

//function to get definition of clicked word
function get_definition_of_clicked_word() {
  $("#text-layer")
    .off()
    .on("click", function(e) {
      if (e.target.nodeName == "SPAN") {
        //if the clicked element is a span show the definition of the text content of the span
        $(function() {
          $(e.target)
            .popover({
              html: true,
              trigger: "click", //<--- you need a trigger other than manual
              delay: {
                show: "500",
                hide: "100"
              }
            })
            .popover("show");
        });

        //if the span has not yet been clicked get definition of the text content
        if (e.target.getAttribute("data-content") == "getting definition....") {
          let define_word = get_definition_from_lexicala(
            e.target.textContent.toLowerCase()
          );
          define_word.then(function(word) {
            if (word != false) {
              data_content = "";
              for (let i = 0; i < word.length; i++) {
                text = "";
                title = word[i]["word"];
                type = word[i]["type"];
                definitions = word[i]["definitions_array"];
                definitions_in_text = [];
                definitions.forEach(function(definition) {
                  definitions_in_text += "-" + definition.trim() + "<br/>";
                });
                text = `${i +
                  1}-<strong>${title}</strong> <i>${type}</i><br/>${definitions_in_text}`;
                data_content += text + "<br/>";
              }

              e.target.setAttribute("data-content", data_content);
              e.target.setAttribute(
                "data-original-title",
                e.target.textContent
              );
              e.target.setAttribute("data-placement", determine(e));
            }
            //esle if the definition of the word in the span has not been fount
            else {
              e.target.setAttribute("data-placement", determine(e));
              e.target.setAttribute(
                "data-content",
                "no definition for that word was found"
              );
            }

            $(function() {
              $(e.target)
                .popover({
                  html: true,
                  trigger: "click", //<--- you need a trigger other than manual
                  delay: {
                    show: "500",
                    hide: "100"
                  }
                })
                .popover("show");
            });
          });
        }
        //else if the span has already been clicked no need to get its defintion just show popovser
        else {
          $(function() {
            $(e.target)
              .popover({
                html: true,
                trigger: "click", //<--- you need a trigger other than manual
                delay: {
                  show: "500",
                  hide: "100"
                }
              })
              .popover("show");
          });
        }
      }
    });
}

//function to get definitions of a word
function get_definition_from_lexicala(get) {
  h = new Headers();
  let encoded = window.btoa("namangala:ilovecoding1@");
  h.append("Authorization", "Basic " + encoded);
  const word = fetch(
    `https://dictapi.lexicala.com/search?source=global&language=en&text=${get}&morph=true`,

    {
      method: "GET",
      headers: h
    }
  )
    .then(function(res) {
      return res.json();
    })
    .then(function(data) {
      if (data["results"].length > 0) {
        all_words = [];
        for (let i = 0; i < data["results"].length; i++) {
          let word = data["results"][i]["headword"]["text"];
          let type = data["results"][i]["headword"]["pos"];
          let definitions_array = [];
          let definitions_in_json = data["results"][i]["senses"];
          definitions_in_json.forEach(function(item) {
            if (item["definition"] !== undefined)
              definitions_array.push(item["definition"]);
          });
          let full_word = {
            word: word,
            type: type,
            definitions_array: definitions_array
          };
          all_words.push(full_word);
        }
        return all_words;
      } else {
        all_words = false;
        return all_words;
      }
    });
  return word;
}

//function to make words clickable
function make_words_clickable() {
  let text_layer = document.getElementById("text-layer");
  let children = text_layer.children;
  for (let i = 0; i < children.length; i++) {
    if (children[i].nodeName != "SPAN") {
      children[i].innerHTML = children[i].textContent.replace(
        /(\w+)/g,
        `<span  class='word' data-html='true' data-content='getting definition....' data-toggle='popover' >$1</span>`
      );
    }
  }
  //callthe function which will be able to get definition of a word
  get_definition_of_clicked_word();

  $(function() {
    $('[data-toggle="popover"]').popover({
      trigger: "click", //<--- you need a trigger other than manual
      delay: {
        show: "500",
        hide: "100"
      }
    });
  });
}

//function to show pdf
function showPDF(pdf_url) {
  $("#pdf-loader").show();
  PDFJS.getDocument({ url: pdf_url })
    .then(function(pdf_doc) {
      __PDF_DOC = pdf_doc;
      __TOTAL_PAGES = __PDF_DOC.numPages;

      // Hide the pdf loader and show pdf container in HTML
      $("#pdf-loader").hide();
      $("#pdf-contents").show();
      $("#pdf-total-pages, #pdf-total-pages-bottom").text(__TOTAL_PAGES);

      // Show the first page
      showPage(1);
      $("#pdf-prev").css("opacity", "0.2");
      // $("#pdf-prev").attr("disabled", true);
    })
    .catch(function(error) {
      // If error re-show the upload button
      $("#pdf-loader").hide();
      $("#upload-button").show();

      alert(error.message);
    });
}

function showPage(page_no) {
  __PAGE_RENDERING_IN_PROGRESS = 1;
  __CURRENT_PAGE = page_no;

  // Disable Prev & Next buttons while page is being loaded
  $("#pdf-next, #pdf-prev, #pdf-next-bottom, #pdf-prev-bottom").attr(
    "disabled",
    "disabled"
  );

  // While page is being rendered hide the canvas and show a loading message
  $("#pdf-canvas").hide();
  $("#page-loader").show();

  // Update current page in HTML
  $("#pdf-current-page, #pdf-current-page-bottom").text(page_no);

  // Fetch the page
  __PDF_DOC.getPage(page_no).then(function(page) {
    // As the canvas is of a fixed width we need to set the scale of the viewport accordingly

    __CANVAS.width = Math.floor(
      Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
    );
    if (__CANVAS.width > 992) {
      __CANVAS.width = 992;
    }
    var scale_required = __CANVAS.width / page.getViewport(1).width;

    // Get viewport of the page at required scale
    var viewport = page.getViewport(scale_required);

    // Set canvas height
    __CANVAS.height = viewport.height;

    var renderContext = {
      canvasContext: __CANVAS_CTX,
      viewport: viewport
    };

    // Render the page contents in the canvas
    page
      .render(renderContext)
      .then(function() {
        __PAGE_RENDERING_IN_PROGRESS = 0;
        if (__PAGE_RENDERING_IN_PROGRESS == 0) {
          setTimeout(make_words_clickable, 5000);
        }
        // Re-enable Prev & Next buttons
        if (page_no != __TOTAL_PAGES) {
          $("#pdf-next, #pdf-next-bottom")
            .removeAttr("disabled")
            .css("opacity", "1");
        } else {
          $("#pdf-next, #pdf-next-bottom")
            .attr("disabled", true)
            .css("opacity", "0.3");
        }

        if (page_no != 1) {
          $("#pdf-prev, #pdf-prev-bottom")
            .removeAttr("disabled")
            .css("opacity", "1");
        } else {
          $("#pdf-prev, #pdf-prev-bottom")
            .attr("disabled", true)
            .css("opacity", "0.3");
        }

        // Show the canvas and hide the page loader
        $("#pdf-canvas").show();
        $("#page-loader").hide();

        // Return the text contents of the page after the pdf has been rendered in the canvas
        return page.getTextContent();
      })
      .then(function(textContent) {
        // Get canvas offset
        var canvas_offset = $("#pdf-canvas").offset();

        // Clear HTML for text layer
        $("#text-layer").html("");

        // Assign the CSS created to the text-layer element
        $("#text-layer").css({
          left: canvas_offset.left + "px",
          top: canvas_offset.top + "px",
          height: __CANVAS.height + "px",
          width: __CANVAS.width + "px"
        });

        // Pass the data to the method for rendering of text over the pdf canvas.
        PDFJS.renderTextLayer({
          textContent: textContent,
          container: $("#text-layer").get(0),
          viewport: viewport,
          textDivs: []
        });
      });
  });
}

// Upon click this should should trigger click on the #file-to-upload file input element
$("#upload-button").on("click", function() {
  $("#file-to-upload").trigger("click");
});
$("#upload-btn").on("click", function() {
  $("#file-to-upload").trigger("click");
});

// When user chooses a PDF file
$("#file-to-upload").on("change", function() {
  // Validate whether PDF

  if (
    ["application/pdf"].indexOf($("#file-to-upload").get(0).files[0].type) == -1
  ) {
    alert("Error : Not a PDF");
    return;
  }

  $("#upload-button").hide();
  $(".hide-in-view").each(function() {
    $(this).hide();
  });

  // Send the object url of the pdf
  showPDF(URL.createObjectURL($("#file-to-upload").get(0).files[0]));
});

// Previous page of the PDF
$("#pdf-prev, #pdf-prev-bottom").on("click", function() {
  if (__CURRENT_PAGE != 1) showPage(--__CURRENT_PAGE);
});

// Next page of the PDF
$("#pdf-next, #pdf-next-bottom").on("click", function() {
  if (__CURRENT_PAGE != __TOTAL_PAGES) showPage(++__CURRENT_PAGE);
});

// $('[data-toggle="popover"]').popover();

//if user clicks anywhere apart from the popover it disappears
$("body").on("click", function(e) {
  $('[data-toggle="popover"]').each(function() {
    //the 'is' for buttons that trigger popups
    //the 'has' for icons within a button that triggers a popup
    if (
      !$(this).is(e.target) &&
      $(this).has(e.target).length === 0 &&
      $(".popover").has(e.target).length === 0
    ) {
      $(this).popover("hide");
    }
  });
});

//show current year in footer
let date = new Date().getFullYear();

$("#footer-info").html("Copyright&copy; DefineIt " + date);
