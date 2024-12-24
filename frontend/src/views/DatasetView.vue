<script>
import {ref, onMounted} from 'vue';
import axios from '@/axios';

export default {
    setup() {
        const datasets = ref([]);

        const name = ref('');
        const description = ref('');
        const language = ref('')

        const handleCreateProject = async () => {
            try {
                response = await axios.post(
                    `http://127.0.0.1:81/api/users/project/`,
                    {
                        name: name.value,
                        description: description.value,
                        language: language.value,
                    },
                );
            } catch (error) {
                console.error('Error creating project', error);
            }
        };

        onMounted(async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:81/api/users/dataset/`);
                datasets.value = response.data.data;
            } catch (error) {
                console.error('Error fetching datasets', error)
            }
        });
        return {
            datasets,
            name,
            description,
            language,
            handleCreateProject
        }
    }
}
</script>

<template>
    <div class="uk-container uk-container-xlarge">
        <div class="uk-navbar">
            <div class="uk-navbar-left">
                <h2>
                    <span class="uk-icon uk-margin-small-right"
                        uk-icon="icon: database; ratio: 2">
                    </span>
                    Датасет (0)
                </h2>
            </div>
            <div class="uk-navbar-right">

            </div>
        </div>

        <table class="uk-table uk-table-middle uk-table-divider">
            <thead>
                <tr>
                    <th>Название проекта</th>
                    <th class="uk-center">Язык программирования</th>
                    <th class="uk-center">Активные уязвимости</th>
                    <th class="uk-center">Статус</th>
                    <th class="uk-center">Последнее взаимодействие</th>
                    <th class="uk-center">Дата подключения</th>
                </tr>
            </thead>
            <tbody>

                <tr>
                    <td>
                        <a href="#" class="uk-button uk-button-text">VulnApp Django</a>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-default">
                            Python
                        </span>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-danger">
                            12
                        </span>
                    </td>
                    <td class="uk-center">
                        <span class="uk-label uk-label-success">
                            Online
                        </span>
                    </td>
                    <td class="uk-center">5 сентября 2015, 14:10</td>
                    <td class="uk-center">5 сентября 2015, 14:10</td>
                </tr>

            </tbody>
        </table>
    </div>
</template>
