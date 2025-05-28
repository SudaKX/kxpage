<template>
  <FrameWrapper>
    <div class="top-container">

      <div class="section tp-wx">
        <a class="link" href="https://www.baidu.com/" target="_blank"></a>
        <img src="../assets/images/wx.png" alt="bg"/>
        <div class="title">
          <img class="icon" src="../assets/images/wechat.png" alt="icon"/>
          <div class="text">微信公众号</div>
        </div>
        <div class="color-vfx"></div>
      </div>

      <div class="section tp-bili">
        <a class="link" href="https://www.baidu.com/" target="_blank"></a>
        <img src="../assets/images/bilibili.png" alt="bg"/>
        <div class="title">
          <img class="icon" src="../assets/images/bili_icon.png" alt="icon"/>
          <div class="text">BiliBili</div>
        </div>
        <div class="color-vfx"></div>
      </div>

      <div class="section tp-author" ref="contributeSection">
        <div class="contributors">
          <div class="inner">
            <div class="avatars">
              <div class="avatar" v-for="contributor, idx in contributors" :key="idx">
                <img :src="'/avatars/' + contributor.path"/>
                <a v-if="contributor.href !== null" :href="contributor.href" target="_blank"></a>
              </div>
            </div>
            <div class="comment">
              前往仓库查看完整列表，以上排名不分先后。
            </div>
          </div>
        </div>
        <img src="../assets/images/author.png" alt="bg"/>
        <div class="title">
          <img class="icon" src="../assets/images/members.png" alt="icon"/>
          <div class="text">贡献者</div>
        </div>
        <div class="color-vfx"></div>
      </div>

      <div class="section tp-repo">
        <a class="link" href="https://github.com/SudaKX/kxpage" target="_blank"></a>
        <img src="../assets/images/repo.png" alt="bg"/>
        <div class="title">
          <img class="icon" src="../assets/images/repo_icon.png" alt="icon"/>
          <div class="text">网站仓库</div>
        </div>
        <div class="color-vfx"></div>
      </div>

    </div>
    <div class="overlay">
      <div class="text animate">MORE CONTENT</div>
    </div>
    <div class="background"></div>
  </FrameWrapper>
</template>

<script setup lang="ts">
import FrameWrapper from '@/components/FrameWrapper.vue';

interface AvatarDescription {
  path: string,
  href?: string
}

const contributors: Array<AvatarDescription> = [
  {path: "darksky.jpg", href: "https://github.com/DarkskyX15"},
  {path: "silver_akatoki.png", href: "https://github.com/SilverAkatoki"}
]

</script>

<style scoped>
  div.overlay {
    left: -1%;
    pointer-events: none;
    position: absolute;
    bottom: -1%;
    width: 102%;
    height: 14%;

    overflow: hidden;

    z-index: 3;

    div.text {
      position: absolute;
      left: 5%;
      font-size: 8vmin;
      font-family: 'Times New Roman', Times, serif;
      font-weight: bold;
      color: var(--kx-dark-neglect);
    }

  }

  div.background {
    pointer-events: none;
    position: absolute;
    height: 28%;
    width: 100%;
    bottom: 0%;
    background-color: var(--kx-dark-black0);
    mask-image: linear-gradient(rgba(0,0,0,0), var(--kx-dark-black0) 60%);
    mask-mode: alpha;
    z-index: 2;
  }

  div.top-container {
    position: absolute;
    height: 100%;
    width: 100%;
    background-color: var(--kx-dark-black0);

    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: space-evenly;

    padding-top: 5%;

    div.section {
      position: relative;
      height: 90%;
      width: 20%;
      background-color: transparent;
      overflow: hidden;

      transition:
        scale 400ms ease,
        box-shadow 400ms ease;

      a.link {
        display: block;
        position: absolute;
        height: 90%;
        width: 100%;
      }

      div.contributors {
        position: absolute;
        background-color: transparent;
        width: 100%;
        height: 70%;

        div.inner {
          position: absolute;
          background-color: var(--kx-dark-activate);
          left: 10%;
          top: 15%;
          width: 80%;
          height: 80%;
          opacity: 0;

          transition:
            opacity 400ms ease,
            box-shadow 400ms ease;
          
          div.avatars {
            position: absolute;
            top: 5%;
            height: 80%;
            width: 100%;

            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: left;
            align-content: flex-start;
            container-type: size;

            mask-image: linear-gradient(rgba(0,0,0,1) 80%, rgba(0,0,0,0));
            mask-mode: alpha;

            div.avatar {
              position: relative;
              width: 16cqw;
              height: 16cqw;
              border-radius: 50%;
              overflow: hidden;
              margin: 2cqw;
              background-color: var(--kx-dark-neglect);
              border: 3px solid var(--kx-dark-neglect);

              img {
                position: absolute;
                height: 100%;
                width: 100%;
              }

              a {
                position: absolute;
                width: 100%;
                height: 100%;
                z-index: 1;
              }

            }
          }

          div.comment {
            pointer-events: none;
            position: absolute;
            top: 85%;
            width: 100%;
            padding: 2%;
            color: var(--kx-dark-neglect);
            text-align: center;
          }

        }
      }

      img {
        position: absolute;
        height: 100%;
        width: 100%;
        object-position: center;
        object-fit: cover;
        z-index: -2;
      }

      div.color-vfx {
        position: absolute;
        height: 100%;
        width: 100%;
        mask-image: linear-gradient(
          rgba(0,0,0,0.0) 50%,
          rgba(0,0,0,1.0)
        );
        mask-mode: alpha;

        transition: background-color 400ms ease;
        z-index: -1;
      }

      div.title {
        position: absolute;
        pointer-events: none;
        bottom: 16%;
        left: 0%;
        width: 100%;
        opacity: 0;

        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;

        transition: opacity 400ms ease;

        img.icon {
          position: relative;
          height: 4vmin;
          width: 4vmin;
          margin: 1vmin;
          object-fit: contain;
        }

        div.text {
          position: relative;
          font-size: 3vmin;
          font-weight: bold;
          color: var(--kx-dark-white0);
        }

      }

    }

    div.section:hover {
      scale: 1.05;
      box-shadow: 10px 10px 0px var(--kx-dark-activate);

      div.title {
        opacity: 1;
      }

      div.contributors div.inner {
        opacity: 1;
        box-shadow: 10px 10px 0px var(--kx-dark-neglect);
        transition:
          opacity 400ms ease 500ms,
          box-shadow 400ms ease 500ms;
      }
    }

    .tp-wx:hover div.color-vfx {
      background-color: green;
    }
    .tp-bili:hover div.color-vfx {
      background-color: pink;
    }
    .tp-author:hover div.color-vfx {
      background-color: skyblue;
    }
    .tp-repo:hover div.color-vfx {
      background-color: orange;
    }
    
  }

  .forward-enter-from div.animate {
    opacity: 0;
  }
  .forward-enter-active div.animate {
    transition: opacity 400ms ease 700ms;
  }

</style>