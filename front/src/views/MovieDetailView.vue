<template>
  <div class="movie-detail-container">
    <div class="video-container">
      <iframe
      v-if="store.movieVideoKey"
        id="player"
        type="text/html"
        width="1150"
        height="650"
        :src="`https://www.youtube.com/embed/${store.movieVideoKey}?autoplay=1&mute=1&controls=0&showinfo=0`"
        frameborder="0"
        allowfullscreen
      ></iframe>
      <h1 class="movie-title">{{ store.movie.title }}</h1>
    </div>
    <div class="movie-info">
      <div class="movie-detail-child">
        <div class="details-top-row">
          <p class="release-date"><strong><i class="bi bi-calendar-check"></i></strong> {{ store.movie.release_date }}</p>
          <p class="runtime"><strong><i class="bi bi-clock-history"></i></strong> {{ store.movie.runtime }} 분</p>
        </div>
        <p class="rating"><strong><i class="bi bi-star-fill"></i></strong> {{ store.movie.vote_average }}</p>
      </div>
      <div class="movie-detail-child">
        <div>
          <span v-for="genreSel in store.movie.genres" :key="genreSel.id">
            <span v-if="store.genres.find((genre) => genre.tmdb_id === genreSel.id)">
              {{ store.genres.find((genre) => genre.tmdb_id === genreSel.id).name }}&nbsp;
            </span>
          </span>
        </div>
      </div>
      <div class="movie-detail-child">
        <p>{{ store.movie.overview }}</p>
      </div>
      <!--로그인 되어 있으면 좋아요, 싫어요, 찜하기 정상 작동-->
      <div class="d-flex justify-content-start" v-if="userStore.isLogin">
        <div style="margin-right: 30px;">
          <span>
            <i
              class="bi bi-hand-thumbs-up"
              @click="likeMovie(store.movie.id)"
              v-if="!store.liked"
              style="font-size: 2rem; cursor: pointer;"
            ></i>
            <i
              class="bi bi-hand-thumbs-up-fill"
              @click="likeMovie(store.movie.id)"
              v-else
              style="font-size: 2rem; cursor: pointer;"
            ></i>
          </span>
        </div>
        <div style="margin-right: 30px;">
          <span>
            <i
              class="bi bi-hand-thumbs-down"
              @click="hateMovie(store.movie.id)"
              v-if="!store.hated"
              style="font-size: 2rem; cursor: pointer;"
            ></i>
            <i
              class="bi bi-hand-thumbs-down-fill"
              @click="hateMovie(store.movie.id)"
              v-else
              style="font-size: 2rem; cursor: pointer;"
            ></i>
          </span>
        </div>
        <div>
          <span>
            <i
              class="bi bi-plus"
              @click="favoriteMovie(store.movie.id)"
              v-if="!store.favorited"
              style="font-size: 2rem; cursor: pointer;"
            ></i>
            <i
              class="bi bi-check-lg"
              @click="favoriteMovie(store.movie.id)"
              v-else
              style="font-size: 2rem; cursor: pointer;"
            ></i>
          </span>
        </div>
      </div>
      <!--로그인 안 되어 있으면 좋아요, 싫어요, 찜하기 클릭 시 로그인 페이지로 이동-->
      <div class="d-flex justify-content-start" v-else>
        <div style="margin-right: 30px;">
          <i class="bi bi-hand-thumbs-up" @click="loginAlert" style="font-size: 2rem; cursor: pointer;"></i>
        </div>
        <div style="margin-right: 30px;">
          <i class="bi bi-hand-thumbs-down" @click="loginAlert" style="font-size: 2rem; cursor: pointer;"></i>
        </div>
        <i class="bi bi-plus" @click="loginAlert" style="font-size: 2rem; cursor: pointer;"></i>
      </div>

      <div>
        <nav class="d-flex justify-content-center fs-larger">
          <RouterLink :to="{ name: 'related' }" @click="getSimilar(store.movie.id)">비슷한 콘텐츠</RouterLink> | 
          <RouterLink :to="{ name: 'review' }" @click="getMovieReview(store.movie.title)" class="pl-3">리뷰 목록</RouterLink>
        </nav>
        <RouterView />
      </div>
    </div>
  </div>
</template>



<script setup>
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { useUserStore } from '@/stores/user'
import { RouterLink, RouterView } from 'vue-router'
import { useCommunityStore } from '@/stores/community'


const userStore = useUserStore()
const store = useMovieStore()
const communityStore = useCommunityStore()
const router = useRouter()
const route = useRoute()
const showIframe = ref(true);
const likeMovie = (movieId) => {
  store.likeMovie(movieId)
}

const hateMovie = (movieId) => {
  store.hateMovie(movieId)
}

const favoriteMovie = (movieId) => {
  store.favoriteMovie(movieId)
}

const loginAlert = () => {
  window.alert('로그인이 필요합니다!')
  router.push({ name: 'login' })
}

const getSimilar = (movieId) => {
  console.log(movieId)
  store.getSimilar(movieId)
}

const getMovieReview = (movieTitle) => {
  console.log(movieTitle)
  communityStore.getMovieReview(movieTitle)
}

const fetchMovieDetails = (movieId) => {
  store.movieDetail(movieId)
}

store.read_lhf(route.params.movieId)
onMounted(() => {
  fetchMovieDetails(route.params.movieId)
})

watch(() => route.params.movieId, (newMovieId) => {
  fetchMovieDetails(newMovieId)
})

onBeforeRouteLeave((to, from, next) => {
  showIframe.value = false;
  store.movieVideoKey = ''
  store.movie = {}
  next()
})
</script>

<style scoped>
.movie-detail-container {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px;

}

.video-container {
  position: relative;
  width: 1200px;
  height: 600px;
  margin-bottom: 30px;
}

.video-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.85) 60%, rgba(0, 0, 0, 1) 90%);
  pointer-events: none; /* Ensure the gradient doesn't interfere with user interaction */
}

.movie-title {
  position: absolute;
  top: 550px;
  left: 20px;
  z-index: 10;
  font-size: 3rem;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
}

.rating i {
  color: yellow;
}
.movie-info {
  position: absolute;
  top: 700px;
  background-color: rgba(0, 0, 0, 1);
  padding: 20px;
  border-radius: 10px;
  color: white;
  text-align: left;
  max-width: 1200px;
  width: 100%;
  margin-top: 0px;
  /* position: relative; */
  z-index: 5;
}

.movie-detail-child {
  margin: 10px 0;
}

.details-top-row {
  display: flex;
}

.details-top-row p {
  padding-right: 40px;
}

.rating {
  margin-top: 10px;
}

nav {
  margin-top: 20px;
}

nav a {
  color: white;
  text-decoration: none;
  margin: 0 10px;
}

nav a:hover {
  text-decoration: underline;
}

</style>
