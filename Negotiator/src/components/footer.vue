<template>
    <div class="footer">
        <!-- Previous Section -->
        <div class="footer-section previous" :class="{ hidden: !showPrevious }" @click="showPrevious ? handlePreviousClick() : null">
            <div v-if="showPrevious">
                <div class="details">
                    <p>{{ previous }}</p>
                    <p class="highlight">{{ previousDetail }}</p>
                </div>
            </div>
        </div>

        <!-- Next Section -->
        <div class="footer-section next" :class="{ hidden: !showNext }" @click=" showNext ? handleNextClick() : null">
            <div class="details">
                <p>{{ next }}</p>
                <p class="highlight">{{ nextDetail }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="js">
const props = defineProps({
    next: String,
    nextDetail: String,
    previous: String,
    previousDetail: String,
    showPrevious: Boolean,
    showNext: Boolean,
});

const emit = defineEmits(["next-page", "previous-page"]);

const handleNextClick = () => emit("next-page");

const handlePreviousClick = () => emit("previous-page");
</script>

<style scoped>
.footer {
    position: relative;
    bottom: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    background-color: #ffffff;
    border-top: 1px solid #ddd;
    height: 70px;
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out;
}

.footer-section {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.footer-section.hidden {
    pointer-events: none;
    opacity: 0.5;
}

.footer-section.previous {
    border-right: 1px solid #ddd;
}

.footer-section:hover {
    background-color: #f1f1f1;
}

.footer-section .details {
    text-align: center;
}

.footer-section .details p {
    margin: 0;
}

.footer-section .details .highlight {
    font-size: 25px;
    font-weight: bold;
}
</style>