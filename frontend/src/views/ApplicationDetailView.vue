<script>
import axios from 'axios';

export default {
  name: 'ApplicationDetailView',
  data() {
    return {
      item: null,
    };
  },
  created() {
    this.fetchItem();
  },
  methods: {
    async fetchItem() {
      try {
        const response = await axios.get(`http://127.0.0.1:81/api/users/project/${this.$route.params.id}/`);
        this.item = response.data.data;
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
  },
};
</script>

<template>
  <div v-if="item">
    <h1>Детали</h1>
    <p><strong>ID:</strong> {{ item.id }}</p>
    <p><strong>Название:</strong> {{ item.title }}</p>
    <!-- Добавьте другие поля, которые хотите отобразить -->
  </div>
  <div v-else>
    Загрузка...
  </div>
</template>
