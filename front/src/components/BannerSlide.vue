<template>
  <div>
    <div id="carouselExampleDark" class="carousel carousel-dark slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button 
          v-for="(movie, index) in recStore.weekday" 
          :key="index" 
          type="button" 
          :data-bs-target="'#carouselExampleDark'" 
          :data-bs-slide-to="index" 
          :class="{'active': index === 0}" 
          :aria-current="index === 0 ? 'true' : undefined" 
          :aria-label="'Slide ' + (index + 1)">
        </button>
      </div>
      <div class="carousel-inner">
        <div 
          v-for="(movie, index) in recStore.weekday" 
          :key="index" 
          :class="['carousel-item', { 'active': index === 0 }]" 
          data-bs-interval="5000">
          <img :src="`https://image.tmdb.org/t/p/w1280${movie.backdrop_path}`" class="d-block w-100" alt="...">
          <div class="carousel-caption d-none d-md-block">
            <h5>{{ movie.title }}</h5>
            <p class="limited-text">{{ truncateText(movie.overview, 150) }}</p>
            <div class="buttons">
              <div class = "info-button" @click="MovieDetail(movie.pk)">
                상세 정보
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRecommendStore } from '@/stores/recommend';

import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, ref } from 'vue';
const router = useRouter()
const recStore = useRecommendStore();

const truncateText = (text, limit) => {
  if (text.length <= limit) {
    return text;
  }
  return text.substring(0, limit) + '...';
};

const MovieDetail = function(movieId) {
    console.log(movieId)
    router.push({name:'detail', params: {movieId: movieId}})
  }
  const isActive = ref(false);
let intervalId = null;

const startAutoSlide = () => {
  intervalId = setInterval(() => {
    const carouselElement = document.querySelector('#carouselExampleDark');
    if (carouselElement) {
      const bsCarousel = new bootstrap.Carousel(carouselElement);
      bsCarousel.next();
    }
  }, 5000);
};


const stopAutoSlide = () => {
  clearInterval(intervalId);
};

onMounted(() => {
  if (!isActive.value) {
    startAutoSlide();
    isActive.value = true;
  }
});

onUnmounted(() => {
  stopAutoSlide();
  isActive.value = false;
});

</script>

<style scoped>
.carousel-item {
  position: relative;
}

.carousel-item::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 10%, rgba(0, 0, 0, 0.9) 90%, rgba(0, 0, 0, 1) 98%);
  z-index: 1;
}

.carousel-item img {
  height: 700px;
  object-fit: cover;
  z-index: 0;
}

.carousel-caption {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  text-align: left;
  width: 100%;
  left: 15%;
  z-index: 2;
}

.carousel-caption h5 {
  font-size: 2rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 2px 2px 4px black;
}

.carousel-caption .limited-text {
  font-size: 1.25rem;
  color: #ddd;
  max-width: 30%;
  margin-top: 0.5rem;
  text-shadow: 2px 2px 4px black;
}

.info-button {
  color: white;
  font-size: 18px;
  padding: 10px 25px;
  background-color: rgba(170, 170, 170, 0.55);
  margin-left: 10px;
  border-radius: 4px;
}

.buttons {
  padding: 20px 0;
  display: flex;
  font-weight: 350;
  margin-top: 10px;
}
.carousel-indicators {
  bottom: 50px;
  top: auto;
}
</style>
