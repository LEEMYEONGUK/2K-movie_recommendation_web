<template>
  <div class="bg-black">
    <div class="banner">
      <BannerSlide />
    </div>
    <!-- 메인 콘텐츠 -->
    <div v-if="userStore.isLogin" class="main-content">
      <div class="category-list">
        <div v-if="store.favoriteMovies.length">
          <div class="category">
            <h3 class="title">찜한 영화 목록</h3>
            <div id="favoriteCarousel" class="carousel slide" data-bs-ride="carousel">
              <div class="carousel-inner">
                <div v-for="(movieGroup, index) in chunkArray(store.favoriteMovies, 9)" :class="['carousel-item', { active: index === 0 }]" :key="index">
                  <div class="d-flex">
                    <div class="movie" v-for="movie in movieGroup" :key="movie.id" @click="MovieDetail(movie.tmdb_id)">
                      <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="img" alt="...">
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="store.favoriteMovies.length > 9">
                <button class="carousel-control-prev" type="button" data-bs-target="#favoriteCarousel" data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#favoriteCarousel" data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Next</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="category-list">
        <div v-if="RecStore.userRecommendMovies.length">
          <div class="category">
            <h3 class="title">{{ userStore.loginUsername }} 님! 이런 영화는 어떠신가요?</h3>
            <div id="usercarouselExampleControls" class="carousel slide" data-bs-ride="carousel">
              <div class="carousel-inner">
                <div v-for="(movieGroup, index) in chunkArray(RecStore.userRecommendMovies, 9)" :class="['carousel-item', { active: index === 0 }]" :key="index">
                  <div class="d-flex">
                    <div class="movie" v-for="movie in movieGroup" :key="movie.id" @click="MovieDetail(movie.pk)">
                      <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" class="img" alt="...">
                    </div>
                  </div>
                </div>
              </div>
              <button class="carousel-control-prev" type="button" data-bs-target="#usercarouselExampleControls" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
              </button>
              <button class="carousel-control-next" type="button" data-bs-target="#usercarouselExampleControls" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="additional-content">
      <div class="category-list">
        <div class="category">
          <h3 class="title">오늘의 추천 영화들</h3>
          <Date />
        </div>
      </div>
      <div class="category-list">
        <div class="category">
          <h3 class="title">랜덤 추천 영화</h3>
          <Week />
        </div>
      </div>
      <div class="category-list">
        <div class="category">
          <h3 class="title">한국의 최근 인기작들</h3>
          <Korea />
        </div>
      </div>
      <div class="category-list">
        <div class="category">
          <div v-if="RecStore.likedGenres">
        <div v-for="(movies, genre) in RecStore.likedGenres" :key="genre">
            <h3 class="title">{{ genre }}</h3>
            <div :id="`usercarouselExampleControls-${genre}`" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-inner">
                    <GenreRecommend :movies="movies"/>
                </div>
                <button class="carousel-control-prev" type="button" :data-bs-target="`#usercarouselExampleControls-${genre}`" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" :data-bs-target="`#usercarouselExampleControls-${genre}`" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
        </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>

import Date from '@/components/Date.vue'
import Korea from '@/components/Korea.vue'
import Week from '@/components/Week.vue'
import BannerSlide from '@/components/BannerSlide.vue'
import { useMovieStore } from '@/stores/movie'
import { useUserStore } from '@/stores/user'
import { useRecommendStore } from '@/stores/recommend'
import { onMounted } from 'vue'
import GenreRecommend from '@/components/GenreRecommend.vue'
import { useRouter } from 'vue-router'


const store = useMovieStore()
const userStore = useUserStore()
const RecStore = useRecommendStore()
const router = useRouter()

const MovieDetail = function(movieId) {
    console.log(movieId)
    router.push({name:'detail', params: {movieId: movieId}})
  }

// Array를 일정 크기로 나누는 함수
const chunkArray = (array, size) => {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}

onMounted(() => {
  RecStore.userRecommendMovies = []
  RecStore.getLikedGenresWithMovies(userStore.userId)
  store.myFavoriteMovie()
  RecStore.userRecommend()
  RecStore.clearLikedGenres()
})
</script>

<style scoped>

.main-content {
  margin-top: 0px;
  padding: 0px;
}


.category-list {
  display: flex;
  flex-direction: column;
  padding: 0px 20px;
  /* margin-top: 20px; */
}

.category {
  padding-bottom: 10px;
  padding: 10px 30px;
}

.category .title {
  font-size: 18px;
  font-weight: 900;
  color: white;
  padding: 15px 0;
}

.d-flex {
  display: flex;
}

.movie {
  padding: 5px;
  position: relative;
}

.movie:hover {
  transform: scale(1.1);
  transition: 0.3s;
  transition-delay: 0s;
}

.movie img {
  border-radius: 4px;
}

.img {
  width: 180px;
  height: 300px; /* 이미지 높이 추가 */
}

.banner img {
  width: 100%;
}

.heading {
  font-size: 14px;
  color: white;
  padding: 5px;
}

.movie-card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movie-card-container h3 {
  align-self: flex-start;
}

.carousel-control-prev, .carousel-control-next {
  width: 50px; /* 이미지 크기와 동일하게 설정 */
  height: 300px; /* 이미지 크기와 동일하게 설정 */
}

.carousel-control-prev-icon, .carousel-control-next-icon {
  width: 100px; /* 아이콘 크기 조정 */
  height: 100px; /* 아이콘 크기 조정 */
}

.small-carousel-button[disabled] {
  opacity: 0.5;
  pointer-events: none;
}

</style>
