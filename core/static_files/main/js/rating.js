console.log('mohammad');

$(document).ready(function () {
    $('.rating-icons .rating').on('click', function () {
        var ratingValue = $(this).data('value');
        $('#rating').val(ratingValue);

        $('.rating-icons .rating').removeClass('active');
        $(this).addClass('active');

        $(this).prevAll().addClass('active');
    });
});

{/* <div class="mb-3">
    <label for="drink_rating" class="form-label">میزان رضایت شما از نوشیدنی ها</label>
    <input type="hidden" id="drink_rating" name="drink_rating" class="form-control" required>
        <div class="rating-icons">
            <i data-value="1" class="rating4 bi bi-emoji-frown"></i>
            <i data-value="2" class="rating4 bi bi-emoji-expressionless"></i>
            <i data-value="3" class="rating4 bi bi-emoji-neutral"></i>
            <i data-value="4" class="rating4 bi bi-emoji-smile"></i>
            <i data-value="5" class="rating4 bi bi-emoji-laughing"></i>
        </div>
</div> */}