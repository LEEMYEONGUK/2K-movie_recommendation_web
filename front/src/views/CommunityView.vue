<template>
  <div class="font container">
    <br />
    <RouterView />
    <div class="d-flex justify-content-between">
      <h3 class="font">REVIEW LIST</h3>
      <!-- <RouterLink
        :to="{ name: 'create' }"
        class="main-text btn btn-outline-danger main-text"
      >
        리뷰 작성하기
      </RouterLink> -->
      <div class="reviewCreate">
              <button  class="main-text btn btn-outline-danger main-text" @click="openReviewCreateModal">Review Create</button>
            </div>
    </div>
    <hr class="border border-danger border-2 opacity-50" />
    <div class="movie-card-container">
      <AllReviewList
        v-for="review in paginatedStoreReviews"
        :key="review.id"
        :review="review"
        class="movie-card"
      />
    </div>
    <nav aria-label="Page navigation example" class="pagination-nav">
              <ul class="pagination justify-content-center">
                <li class="page-item px-3" :class="{ disabled: currentStorePage === 1 }">
                  <a class="page-link" href="#" @click.prevent="prevStorePage" tabindex="-1" :aria-disabled="currentStorePage === 1">Previous</a>
                </li>
                <li class="page-item px-3">
                  <a class="page-link" href="#">{{ currentStorePage }} / {{ totalStorePages }}</a>
                </li>
                <li class="page-item px-3" :class="{ disabled: currentStorePage === totalStorePages }">
                  <a class="page-link" href="#" @click.prevent="nextStorePage" :aria-disabled="currentStorePage === totalStorePages">Next</a>
                </li>
              </ul>
        </nav>
    <hr class="border border-danger border-2 opacity-50" />
    <div v-if="isReviewCreateModalOpen" class="modal-overlay-reviewcreate" @click.self="closeReviewCreateModal">
        <div class="modal-content-reviewcreate">
          <div>
            <button class="close-reviewcreate" @click="closeReviewCreateModal"><i class="bi bi-x-circle-fill"></i></button>
          </div>
          <div>
            <ReviewCreate @close="closeReviewCreateModal" :close-modal="closeReviewCreateModal" />
          </div>
        </div>
      </div>
  </div>
</template>

<script setup>
import AllReviewList from "@/components/AllReviewList.vue";
import { onMounted, ref, computed } from "vue";
import { useCommunityStore } from "@/stores/community";
import ReviewCreate from "@/components/ReviewCreate.vue";

const store = useCommunityStore();
const isReviewCreateModalOpen = ref(false)
onMounted(() => {
  store.getReviews();
});
const openReviewCreateModal = () => {
  isReviewCreateModalOpen.value = true
}

const closeReviewCreateModal = () => {
  isReviewCreateModalOpen.value = false
}
const currentStorePage = ref(1);
const itemsPerStorePage = 15;
const paginatedStoreReviews = computed(() => {
  const start = (currentStorePage.value - 1) * itemsPerStorePage;
  const end = start + itemsPerStorePage;
  return store.reviews.slice(start, end);
});

const totalStorePages = computed(() => {
  return Math.ceil(store.reviews.length / itemsPerStorePage);
});

const prevStorePage = () => {
  if (currentStorePage.value > 1) currentStorePage.value--;
};

const nextStorePage = () => {
  if (currentStorePage.value < totalStorePages.value) currentStorePage.value++;
};

const goToStorePage = (page) => {
  currentStorePage.value = page;
};

</script>

<style scoped>
.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px; /* 카드 간격을 조정합니다 */
}

.movie-card {
  flex: 1 1 calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  max-width: calc(16.666% - 20px); /* 6개의 열을 기본으로 합니다 */
  margin: 10px; /* 카드 간격을 조정합니다 */
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
.pagination-nav {
  margin-top: 100px; /* 페이지 네비게이션을 30px 아래로 내립니다 */
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

.main-text {
  font-size: 20px;
  font-weight: 900;
}
.modal-overlay-reviewcreate {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 상단에 정렬 */
  z-index: 1100; /* 네비게이션 바 위에 위치 */
}
.modal-content-reviewcreate {
  background-color: rgb(0, 0, 0);
  padding: 10px;
  border-radius: 3px;
  width: 80%;
  max-width: 600px;
  max-height: 80%;
  overflow-y: auto;
  position: relative;
}
.close-reviewcreate {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: red;
  z-index: 1200; /* z-index 추가 */
}

</style>

