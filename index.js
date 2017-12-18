<!DOCTYPE html>
<html>
  <head>
    <title>Lapor Classifier</title>
    <link rel="stylesheet" type="text/css" href="jqcloud.css" />
    <style>
      @import url('https://fonts.googleapis.com/css?family=Istok+Web');
      @import url('https://fonts.googleapis.com/css?family=Lora');

      h1 {
        font-family: 'Istok Web', sans-serif;
      }

      p {
        font-family: 'Lora', serif;
      }

      .cloud {
        display: inline-block;
      }

      .left {
        margin-left: auto;
      }

      .right {
        margin-right: auto;
      }
    </style>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
    <script type="text/javascript" src="jqcloud-1.0.4.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {
      var word_array = [];
        
      $.ajax({
          type: "GET",
          url: "output.csv",
          dataType: "text",
          success: function(data) {processData(data);}
      });

    function processData(allText) {
      var allTextLines = allText.split(/\r\n|\n/);
      var headers = allTextLines[0].split(',');
      var lines = [];

      for (var i=1; i<allTextLines.length; i++) {
          var data = allTextLines[i].split(',');
          if (data.length == headers.length) {

              var tarr = [];
              for (var j=0; j<headers.length; j++) {
                  tarr.push(data[j]);
              }
              lines.push(tarr);
          }
      }
      var counter=1;
      for(var i = 0; i < lines.length; i++){
        var line=lines[i];
        if(line[0]!=counter || i==lines.length-1){
          if(i==lines.length-1){
            word_array.push({text: line[1], weight: parseFloat($.trim(line[2]))});
          }
          var id="#wordcloud" + counter;
          console.log(id);
          $(id).jQCloud(word_array);
          word_array = [];
          counter++;
        }
        word_array.push({text: line[1], weight: parseFloat($.trim(line[2]))});
      }
    }
    });

    </script>
  </head>
  <body>
    <h1>Lapor Classifier</h1>
    <p>Lapor Classifier is a data visualization webpage providing
      insights on lapor.go.id topic distribution.
        Since lapor.go.id do not have tags feature, 
        this application purpose is to create relevant tags and to visualize 
        the big picture of all lapor.go.id entries. 
        Using Latent Dirichlet Allocation (LDA) for the topic modelling. Built with Python &amp; jQCloud.
        <br/>Created as the fourth assignment of Information Retrieval course (IKO41357).
    </p>

    <div id="wordcloud1" class="cloud left" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud2" class="cloud right" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud3" class="cloud left" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud4" class="cloud right" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud5" class="cloud left" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud6" class="cloud right" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud7" class="cloud left" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud8" class="cloud right" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud9" class="cloud left" style="width: 550px; height: 350px;"></div>
    <div id="wordcloud10" class="cloud right" style="width: 550px; height: 350px;"></div>
  </body>
</html>