<template>
  <div class="review-create-container">
    <form @submit.prevent="updateReview">
      <div class="form-group">
        <label for="movie_title_search">영화 제목</label>
        <input
          class="form-control"
          v-model="query"
          @input="searchMovies"
          placeholder="Search for a movie"
          id="movie_title_search"
          name="movie_title_search"
        />
        <ul v-if="movies.length" class="search-results">
          <li
            v-for="movie in movies"
            :key="movie.id"
            class="search-result__card"
            @click="selectMovie(movie.title, movie.poster_path)"
          >
            <img
              class="img"
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
              alt="..."
            />
            {{ movie.title }}
          </li>
        </ul>
      </div>

      <div>
        <input
          type="hidden"
          id="movie_title"
          name="movie_title"
          v-model="movie_title"
        />
      </div>

      <div class="form-group">

        <input
          class="form-control"
          type="text"
          id="title"
          name="title"
          v-model="title"
        />
      </div>

      <div class="form-group">

        <textarea
          class="form-control"
          type="text"
          id="content"
          name="content"
          v-model="content"
        ></textarea>
      </div>
      <div>
        <label class="form-group" for="rank">나의 점수</label>
        <StarRating v-model="rank" />
      </div>

      <button class="mt-3 btn btn-outline-danger main-text" type="submit">
        수정하기
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCommunityStore } from "@/stores/community";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import StarRating from "@/components/StarRating.vue";

const props = defineProps({
  review: Object
});

const emit = defineEmits(['close']);

// 리뷰 작성 필드 정보
const title = ref(props.review.title);
const movie_title = ref(props.review.movie_title);
const rank = ref(props.review.rank);
const content = ref(props.review.content);
const poster_path = ref(props.review.poster_path);

// 검색 변수
const query = ref(props.review.movie_title);
const movies = ref([]);

// 검색 기능
const searchMovies = async () => {
  if (query.value.length >= 2) {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/v1/search/", {
        params: {
          query: query.value,
        },
      });
      movies.value = response.data.results;
    } catch (error) {
      console.error("영화 정보를 가져오는 중 오류 발생:", error);
    }
  } else {
    movies.value = [];
  }
};

// 영화 선택
const selectMovie = (title, path) => {
  movie_title.value = title;
  query.value = title;
  poster_path.value = path;

  searchMovies();
};

// 리뷰 수정
const updateReview = function () {
  const data = {
    title: title.value,
    movie_title: movie_title.value,
    content: content.value,
    rank: rank.value,
    user: useUserStore().userId,
    poster_path: poster_path.value,
    username: useUserStore().loginUsername,
    reviewId: props.review.id
  };
  useCommunityStore().updateReview(data);

  emit('close');
};
</script>

<style scoped>
input:focus {
  outline: 2px solid rgb(255, 0, 0);
}

.img {
  width: 100px;
}
.main-text {
  font-size: 20px;
}

.search-result__card:hover {
  cursor: pointer;
  color: white;
  background-color: #ec3c39;
}
.review-create-container {
  background-color: black;
  color: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 14px 28px rgba(44, 44, 44, 0.25),
    0 10px 10px rgba(15, 15, 15, 0.22);
}
.form-group {
  margin-bottom: 15px;
}
label {
  margin-bottom: 5px;
  font-weight: bold;
}
.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #333;
  color: white;
}
</style>
