import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useUserStore } from './user'

export const useRecommendStore = defineStore('recommend', () => {
  const weekday = ref([])
  const koMovies = ref([])
  const weekMovies = ref([])
  const likedGenres = ref([])
  const userRecommendMovies = ref([])
  const userStore = useUserStore()

  const getTodayRecommend = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/recommend/weekday/'
    })
    .then((res) => {

      weekday.value = res.data
    })
  }

  const getKoreanMovies = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/recommend/korea/'
    })
    .then((res) => {

      koMovies.value = res.data
    })
  }

  const getWeekMovies = function() {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/recommend/week/'
    })
    .then((res) => {

      weekMovies.value = res.data
    })
  }

  const getLikedGenresWithMovies = function(userId) {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/movies/liked_genres/${userId}/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then((res) => {

      likedGenres.value = res.data
    })
  }

  const clearLikedGenres = function() {
    likedGenres.value = []
  }
  const userRecommend = function() {
    userRecommendMovies.value = []
    axios({
        method: "post",
        url: `http://127.0.0.1:8000/api/v1/movies/${userStore.userId}/user_recommend/`,
        headers: {
          Authorization: `Token ${userStore.token}`
        }
      }).then((response) => {

        userRecommendMovies.value = response.data
        console.log("유저 맞춤 추천")
      })
        .catch((error) => {
          console.log(error)
      })
  }

  return {
    weekday, 
    getTodayRecommend, 
    koMovies, 
    getKoreanMovies, 
    weekMovies, 
    getWeekMovies, 
    likedGenres, 
    getLikedGenresWithMovies, 
    clearLikedGenres,
    userRecommendMovies,
    userRecommend
  }
}, { persist: true })
