<template>
    <div>
        <ul class="list-group" v-if="users && users.length > 0">
            <li v-for="user in users" :key="user.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <img :src="user.from_user_profile.avatar" alt="avatar" class="rounded-circle me-3" width="50" height="50">
                    <div>
                        <h5 class="mb-0">
                            <a :href="`/wall/${user.from_user_profile.pk}/`" class="friend-name">{{ user.from_user_profile.full_name }}</a>
                        </h5>
                    </div>
                </div>
                <div>
                    <button type="button" class="btn btn-success me-2" @click="acceptFriendRequest(user.from_user)">Добавить</button>
                    <button type="button" class="btn btn-danger" @click="cancelFriendRequest(user.from_user)">Отклонить</button>
                </div>
            </li>
        </ul>
        <p v-else-if="users && users.length === 0" class="text-center">У вас нет входящих запросов на добавление в друзья.</p>
        <p v-else class="text-center">Загрузка данных...</p>
    </div>
</template>

<script>
import axios from 'axios';
import { API_BASE_URL } from '../../config';

export default {
    data() {
        return {
            users: [] // Инициализация пустым массивом
        }
    },
    mounted() {
        this.getIncomingUsers();
    },
    methods: {
        async getIncomingUsers() {
            try {
                const response = await axios.get(`${API_BASE_URL}/relations/received-requests/`, {
                    headers: {
                        'Authorization': `token ${localStorage.getItem('token')}`
                    }
                });
                this.users = response.data;
            } catch (error) {
                console.error('Error fetching friends:', error);
            }
        },
        async acceptFriendRequest(userId) {
            try {
                await axios.put(`${API_BASE_URL}/relations/accept-friend-request/`, null, {
                    headers: {
                        'Authorization': `token ${localStorage.getItem('token')}`
                    },
                    params:{
                        from_user: userId
                    }
                });

                this.users = this.users.filter(user => user.from_user !== userId);
            } catch (error) {
                console.error('Error accepting friend request:', error);
            }
        },
        async cancelFriendRequest(userId) {
            try {
                await axios.delete(`${API_BASE_URL}/relations/cancel-friend-request/`, {
                    headers: {
                        'Authorization': `token ${localStorage.getItem('token')}`
                    },
                    params: {
                        from_user: userId
                    }
                });

                this.users = this.users.filter(user => user.from_user !== userId);
            } catch (error) {
                console.error('Error canceling friend request:', error);
            }
        }
    }
}
</script>

<style scoped>
.friend-name {
    color: inherit;
    text-decoration: none;
}
.list-group-item {
    border: none;
    padding: 15px 20px;
    margin-bottom: 10px;
    background-color: #f8f9fa;
    border-radius: 8px;
}
.text-center {
    text-align: center;
    margin-top: 20px; /* Добавим отступ сверху */
}
</style>
