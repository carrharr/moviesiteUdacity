#!/usr/bin/python

import webbrowser
import os
import re
import server

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        #newMovie {
            border-radius: 4%;
            margin-top: 10px;
        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile-video', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
        // Open More Info Modal when 'More Info' button is clicked
        $(document).on('click', '.btn-info', function (event) {
            var plot = $(this).attr('data-plot');
            var title = $(this).attr('data-title');
            var release = $(this).attr('data-release');
            var rating = $(this).attr('data-rating');
            var genre = $(this).attr('data-genre');
            var director = $(this).attr('data-director');
            var actors = $(this).attr('data-actors');
            $('.plot-info').append(plot);
            $('.modal-title').append(title);
            $('.release-info').append(release);
            $('.rating-info').append(rating);
            $('.genre-info').append(genre);
            $('.director-info').append(director);
            $('.actors-info').append(actors);
        });
        // Close More Info Modal when the 'Close' button is clicked
        $(document).on('click', '.close-modal, #infoModal', function (event) {
            $('.plot-info').empty();
            $('.modal-title').empty();
            $('.release-info').empty();
            $('.rating-info').empty();
            $('.genre-info').empty();
            $('.director-info').empty();
            $('.actors-info').empty();
        });
        // Make all movie tiles have the same height
        // Source: http://stackoverflow.com/questions/23287206/same-height-column-bootstrap-3-row-responsive
        $(document).ready(function() {
            var heights = $(".movie-tile").map(function() {
                return $(this).height();
            }).get(),
            maxHeight = Math.max.apply(null, heights);
            $(".movie-tile").height(maxHeight);
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>


    <!-- Modal -->
    <div id="infoModal" class="modal fade" role="dialog">
        <div class="modal-dialog">

    <!-- Modal content box -->
                <div class="modal-content">
                    <div id="info-modal-container">
                        <div class="modal-header">
                            <h4 class="modal-title text-center"></h4>
                        </div>
                        <div class="modal-body">
                            <h5>Plot</h5>
                            <p class="plot-info"></p>
                            <h5>Release Date</h5>
                            <p class="release-info"></p>
                            <h5>Rating</h5>
                            <p class="rating-info"></p>
                            <h5>Genre</h5>
                            <p class="genre-info"></p>
                            <h5>Director</h5>
                            <p class="director-info"></p>
                            <h5>Actors</h5>
                            <p class="actors-info"></p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="close-modal btn btn-default" data-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    <!-- Main Page Content -->
    <div class="container">
     <!-- <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">"TheStorage" Cinema </a>
          </div>
        </div>
      </div>
    </div> -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="#"><p>"TheStorage" Cinema</p></a>
            </div>
            <!-- Add New Movie Form -->
            <div>
                <ul class="nav navbar-nav pull-right">
                <li>
                    <form action="" method="POST">
                        <input type="text" name="newMovie" id="newMovie" placeholder="Button under Dev">
                        <button type="submit" id="submit" class="btn btn-sm">Submit</button>
                    </form>
                </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- Movie tiles -->
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center">
    <div class="movie-tile-video" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <img src="{poster_image_url}" width="220" height="342">
        <h2>{movie_title}</h2>
    </div>
    <button type="button" class="btn btn-info btn-lg" data-plot="{plot}"
        data-title="{movie_title}" data-release="{release}"
        data-rating="{rating}" data-genre="{genre}"
        data-director="{director}" data-actors="{actors}" data-toggle="modal"
        data-target="#infoModal">More Info</button>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailerYoutubeUrl)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailerYoutubeUrl)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            poster_image_url=movie.posterImageUrl,
            trailer_youtube_id=trailer_youtube_id,
            plot=movie.storyline,
            movie_title=movie.title,
            release=movie.date,
            rating= "IMDB " + movie.rating,
            genre=movie.genre,
            director=movie.director,
            actors=movie.actors,
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('index.html', 'w')


  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output and open the file in browser from server
  output_file.write(main_page_head + rendered_content)
  output_file.close()
  webbrowser.open("http://%(interface)s:%(port)s" % dict(interface=server.I or "localhost", port=server.PORT))
  server.serveSite()
