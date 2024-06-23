<template>
  <div v-if="favoriteMovies.length">
    <div class="cover-container">
      <img
        class="img"
        :src="`https://image.tmdb.org/t/p/w1280${favoriteMovies[randomIndex].backdrop_path}`"
        alt="..."
      />
      <div class="gradient-overlay"></div>
    </div>
  </div>

  <!-- 찜한 영화 없을때, 커버 사진 없음 -->
  <div class="container">
    <div v-if="favoriteMovies.length" class="d-flex align-items-center justify-content-center flex-column">
      <div class="d-flex">
        <div class="box d-flex flex-column align-items-center">
          <img class="profile" src="@/assets/profile.jpg" alt="#" />
          <p class="fs-4 nickname">닉네임 : {{ store.loginUsername }}</p>
        </div>
      </div>
    </div>

    <!-- 찜한 영화 있을 때, 커버 사진 있음 -->
    <div v-else class="d-flex align-items-center justify-content-center flex-column">
      <div class="d-flex">
        <div class="no-box d-flex flex-column align-items-center">
          <img class="profile" src="@/assets/profile.jpg" alt="#" />
          <p class="fs-4 nickname">닉네임 : {{ store.loginUsername }}</p>
        </div>
      </div>
    </div>

    <!-- 작성한 리뷰 목록 -->
    <div class="mt-5" v-if="paginatedReviews.length">
      <h2 class="font">작성한 리뷰 목록</h2>
      <div class="movie-card-container">
        <div v-for="review in paginatedReviews" :key="review.id">
          <div id="box">
            <img
              :src="`https://image.tmdb.org/t/p/w500${review.poster_path}`"
              class="img"
              alt="..."
            />
            <div class="overlay">
              <div class="heading">
                {{ review.movie_title }}
              </div>

              <div class="texts mt-3">리뷰 내용 : {{ review.content }}</div>

              <div class="texts mt-3">
                좋아요 : {{ review.like_users.length }}
              </div>

              <button
                class="btn btn-outline-danger mt-3 mb-5"
                @click="goDetail(review.id)"
              >
                리뷰 상세 내용 보기
              </button>
            </div>
          </div>
        </div>
      </div>
      <nav aria-label="Page navigation example" class="pagination-nav">
        <ul class="pagination justify-content-center">
          <li class="page-item px-3" :class="{ disabled: currentPageReviews === 1 }">
            <a class="page-link" href="#" @click.prevent="prevPageReviews" tabindex="-1" :aria-disabled="currentPageReviews === 1">Previous</a>
          </li>
          <li class="page-item px-3" v-for="page in totalPagesReviews" :key="page" :class="{ active: currentPageReviews === page }">
            <a class="page-link" href="#" @click.prevent="goToPageReviews(page)">{{ page }}</a>
          </li>
          <li class="page-item px-3" :class="{ disabled: currentPageReviews === totalPagesReviews }">
            <a class="page-link" href="#" @click.prevent="nextPageReviews" :aria-disabled="currentPageReviews === totalPagesReviews">Next</a>
          </li>
        </ul>
      </nav>
    </div>

    <!-- 찜한 영화 목록 -->
    <div class="mt-5" v-if="paginatedFavoriteMovies.length">
      <h2 class="font">찜한 영화 목록</h2>
      <div class="movie-card-container">
        <div v-for="movie in paginatedFavoriteMovies" :key="movie.id">
          <div id="box">
            <img
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
              class="img"
              alt="..."
            />
            <div class="overlay">
              <h1 class="heading">
                {{ movie.title }}
              </h1>
              <button class="btn btn-outline-danger mt-3 mb-3" @click="MovieDetail(movie.tmdb_id)">
                영화 상세 보기
              </button>
            </div>
          </div>
        </div>
      </div>
      <nav aria-label="Page navigation example" class="pagination-nav">
        <ul class="pagination justify-content-center">
          <li class="page-item px-3" :class="{ disabled: currentPageFavorites === 1 }">
            <a class="page-link" href="#" @click.prevent="prevPageFavorites" tabindex="-1" :aria-disabled="currentPageFavorites === 1">Previous</a>
          </li>
          <li class="page-item px-3" v-for="page in totalPagesFavorites" :key="page" :class="{ active: currentPageFavorites === page }">
            <a class="page-link" href="#" @click.prevent="goToPageFavorites(page)">{{ page }}</a>
          </li>
          <li class="page-item px-3" :class="{ disabled: currentPageFavorites === totalPagesFavorites }">
            <a class="page-link" href="#" @click.prevent="nextPageFavorites" :aria-disabled="currentPageFavorites === totalPagesFavorites">Next</a>
          </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useUserStore();
const user = ref({});
const favoriteMovies = ref([]);
const reviews = ref([]);
const randomIndex = ref(0);

const currentPageReviews = ref(1);
const currentPageFavorites = ref(1);
const itemsPerPage = 8;

const paginatedReviews = computed(() => {
  const start = (currentPageReviews.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return reviews.value.slice(start, end);
});

const paginatedFavoriteMovies = computed(() => {
  const start = (currentPageFavorites.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return favoriteMovies.value.slice(start, end);
});

const totalPagesReviews = computed(() => Math.ceil(reviews.value.length / itemsPerPage));
const totalPagesFavorites = computed(() => Math.ceil(favoriteMovies.value.length / itemsPerPage));

const prevPageReviews = () => {
  if (currentPageReviews.value > 1) currentPageReviews.value--;
};

const nextPageReviews = () => {
  if (currentPageReviews.value < totalPagesReviews.value) currentPageReviews.value++;
};

const goToPageReviews = (page) => {
  currentPageReviews.value = page;
};

const prevPageFavorites = () => {
  if (currentPageFavorites.value > 1) currentPageFavorites.value--;
};

const nextPageFavorites = () => {
  if (currentPageFavorites.value < totalPagesFavorites.value) currentPageFavorites.value++;
};

const goToPageFavorites = (page) => {
  currentPageFavorites.value = page;
};

// 영화 상세페이지 이동
const MovieDetail = function (movieId) {
  console.log(movieId);
  router.push({ name: "detail", params: { movieId: movieId } });
};

// 리뷰 상세 정보 페이지 이동
const goDetail = function (reviewId) {
  router.push({ name: "reviewDetail", params: { reviewId: reviewId } });
};

// 찜한 영화 조회
const favoriteMovie = function () {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1/movies/${store.userId}/profile_favorite/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      favoriteMovies.value = response.data;
      console.log("프로필 찜한 영화 조회");
      randomIndex.value = Math.floor(
        Math.random() * favoriteMovies.value.length
      );
      console.log(randomIndex.value);
    })
    .catch((error) => {
      console.log(error);
    });
};

// 유저가 작성한 리뷰 조회
const userReview = function () {
  axios({
    method: "get",
    url: `http://127.0.0.1:8000/api/v1_1/reviews/${store.userId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((response) => {
      console.log(response);
      reviews.value = response.data;
      console.log("유저 작성 리뷰 조회");
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  store.profile();
  user.value = store.user;
  favoriteMovie();
  userReview();
});
</script>

<style scoped>
.nickname {
  white-space: nowrap;
}
.box {
  width: 150px;
  height: 150px;
  bottom: 0;
  left: 0;
  transform: translateY(-70%);
}

.no-box {
  width: 150px;
  height: 150px;
  bottom: 0;
  left: 0;
}

.profile {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}
.img {
  width: 50px;
}

/* 커버 이미지 */
.cover-container {
  width: 100%; /* 컨테이너의 너비를 100%로 설정 */
  height: 35vh; /* 컨테이너의 높이를 뷰포트 높이의 50%로 설정 */
  overflow: hidden; /* 컨테이너 밖의 이미지 부분 숨기기 */
  position: relative; /* 이미지 위치 조정을 위한 상대 위치 설정 */
}

.cover-container img {
  width: 100%; /* 이미지의 너비를 컨테이너에 맞춤 */
  height: auto; /* 이미지의 비율을 유지 */
  position: absolute; /* 절대 위치 설정 */
  top: 0; /* 이미지를 컨테이너의 상단에 맞춤 */
  transform: translateY(-5%);
}
.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.9) 90%,
    rgba(0, 0, 0, 1) 98%
  );
  pointer-events: none;
}

.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.movie-card {
  flex: 1 1 calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  max-width: calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  margin: 10px;
  /* 카드 간격을 조정합니다 */
}

@media (max-width: 1200px) {
  .movie-card {
    flex: 1 1 calc(25% - 20px); /* 4개의 열로 조정 */
    max-width: calc(25% - 20px);
  }
}

@media (max-width: 768px) {
  .movie-card {
    flex: 1 1 calc(33.333% - 20px); /* 3개의 열로 조정 */
    max-width: calc(33.333% - 20px);
  }
}

@media (max-width: 480px) {
  .movie-card {
    flex: 1 1 calc(50% - 20px); /* 2개의 열로 조정 */
    max-width: calc(50% - 20px);
  }
}

#box {
  width: 300px;
  height: 500px;
  border-radius: 8px;
  overflow: hidden;
  margin: 50px auto;
  transition: all 0.3s cubic-bezier(0.42, 0, 0.58, 1);
}

#box:hover {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  transform: translateY(-10px);
}
#box * {
  padding: 0 5px;
}

#box .img {
  display: block;
  width: inherit;
  height: inherit;
  padding: 0;
}
#box .heading {
  font-size: 28px;
  color: white;
}

#box .data {
  display: flex;
  flex-direction: column;
  font-size: 12px;
  color: #666;
}

#box .data span {
  padding: 0;
}

#box .data .date {
  margin-bottom: 2px;
}

#box .data .user-id {
  font-size: 16px;
  color: #000;
  font-weight: 600;
}

#box .texts {
  font-size: 16px;
  line-height: 18px;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: inherit;
  height: inherit;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: rgb(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

#box:hover .overlay {
  opacity: 1;
  pointer-events: auto;
}

.pagination-nav {
  margin-top: 30px; /* 페이지 네비게이션을 30px 아래로 내립니다 */
}

.page-item.active .page-link {
  background-color: #000000; /* Bootstrap의 Danger 색상 */
  border-color: #dc3545;
  color: rgb(255, 0, 0);
}

.page-link {
  color: rgb(255, 255, 255); /* 눌리지 않았을 때 검정색 */
  background-color: black;
  border-color: black;
}
.page-item.disabled .page-link {
  background-color: #000000; /* 비활성화된 버튼의 배경색 */
  color: #6c757d; /* 비활성화된 버튼의 텍스트 색상 */
  pointer-events: none; /* 클릭 불가 */
  border-color: black;
}
</style>
