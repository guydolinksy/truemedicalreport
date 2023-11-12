import { Button, Card, Divider as AntdDivider, InputNumber, Menu, Radio, Table, Tag as AntdTag } from 'antd';
import type { FC } from 'react';
import React, { useCallback, useState } from 'react';
import Moment from 'react-moment';
import 'moment';

const Procedures: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="37.56" height="31.617">
    <g data-name="Group 244">
      <path
        fill="none"
        stroke="#6462a3"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="m28.212 1.414-2.389 2.389 7.933 2.389 2.389-2.346m-10.322-.043-3.114 3.114 7.933 2.389 3.114-3.114m-22.009 17.36 3.839-3.881M30.642 9.306l-3.37 3.412-7.933-2.431 3.37-3.37m1.962 7.336q-3.2 1.919-2.431 7.038l-5.033 5.033a14.732 14.732 0 0 1-9.981 4.244l11.3.021m2.986 0h7.422m-9-19.279L1 30.247a29.385 29.385 0 0 0 6.227.32"
        data-name="Path 417"
      />
    </g>
  </svg>
);

const Drugs: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="25.118" height="33.141">
    <g data-name="Group 237">
      <g data-name="Group 236">
        <path
          fill="#6462a3"
          d="M17.55 22.374v-2.9h-3.54v-3.541h-2.9v3.54H7.569v2.9h3.54v3.54h2.9v-3.54Z"
          data-name="Path 411"
        />
      </g>
      <path
        fill="none"
        stroke="#6462a3"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M24.118 30.222a1.606 1.606 0 0 1-.853 1.45 3.8 3.8 0 0 1-2 .469H3.389Q1 32.141 1 30.222V17.341l2.943-4.351v-2.431h-.706a.754.754 0 0 1-.853-.853V1.85a.754.754 0 0 1 .853-.853h18.175a.754.754 0 0 1 .853.853v7.853a.754.754 0 0 1-.853.853h-.194v2.434l2.9 4.351Zm-2.9-19.663H3.943"
        data-name="Path 412"
      />
    </g>
  </svg>
);

const Vitals: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="32.113" height="37.708">
    <g data-name="Group 246">
      <g data-name="Group 231">
        <path
          fill="none"
          stroke="#6462a3"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M21.132 36.658q4.948.213 6.185-.427 1.194-.6-1.408-1.493a43.483 43.483 0 0 0-10.471-1.962q-.994 3.584 5.694 3.882Zm-5.694-3.881q-4.777-.427-10.983-.427H1m21.54-7.72a27.164 27.164 0 0 0-5.89 5.8 7.9 7.9 0 0 0-1.216 2.346"
          data-name="Path 406"
        />
      </g>
      <g data-name="Group 233">
        <g data-name="Group 232">
          <path
            fill="#6462a3"
            d="M11.171 32.437a2.075 2.075 0 0 0-1.221-1.742 6.19 6.19 0 0 0-3.022-.727 5.946 5.946 0 0 0-2.992.673 2.077 2.077 0 0 0-1.295 1.72 2.011 2.011 0 0 0 1.265 1.71 5.74 5.74 0 0 0 2.98.764 5.972 5.972 0 0 0 3.034-.71 2.008 2.008 0 0 0 1.251-1.688Z"
            data-name="Path 407"
          />
        </g>
        <path
          fill="none"
          stroke="#6462a3"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1.7320692800000002"
          d="M6.89 34.818a5.74 5.74 0 0 1-2.98-.763 2.011 2.011 0 0 1-1.264-1.712 2.077 2.077 0 0 1 1.295-1.715 5.946 5.946 0 0 1 2.992-.673 6.191 6.191 0 0 1 3.023.727 2.075 2.075 0 0 1 1.221 1.742 2.008 2.008 0 0 1-1.252 1.689 5.983 5.983 0 0 1-3.036.705Z"
          data-name="Path 408"
        />
      </g>
      <g data-name="Group 235">
        <g data-name="Group 234">
          <path
            fill="#7f939c"
            d="M21.259 5.563a.846.846 0 0 0-.085.384.939.939 0 0 0 .3.682.929.929 0 0 0 .725.341.853.853 0 0 0 .725-.341.939.939 0 0 0 .3-.682 2.169 2.169 0 0 0-.043-.427 2.784 2.784 0 0 0-.256-.3.9.9 0 0 0-.725-.3.847.847 0 0 0-.384.085L20.193 3.9Z"
            data-name="Path 409"
          />
        </g>
        <path
          fill="none"
          stroke="#6462a3"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15.285 4.028h2.346a4.59 4.59 0 0 1 1.066-1.621A4.789 4.789 0 0 1 22.155 1a4.647 4.647 0 0 1 3.412 1.408 5.149 5.149 0 0 1 1.109 1.621h2.175q2.261 0 2.261 2.559v15.27q0 2.559-2.261 2.559H15.285q-2.3 0-2.3-2.559V6.587q0-2.559 2.3-2.559Zm11.388 0a4.892 4.892 0 0 1 .341 1.834 4.954 4.954 0 0 1-4.862 4.862 4.717 4.717 0 0 1-3.455-1.45 4.647 4.647 0 0 1-1.408-3.412 4.892 4.892 0 0 1 .341-1.834"
          data-name="Path 410"
        />
      </g>
    </g>
  </svg>
);

const Other: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="20.947" height="33.558">
    <g data-name="Group 245">
      <path
        fill="none"
        stroke="#6462a3"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M6.853 23.559a4.168 4.168 0 0 0 3.37 3.924m.469-25.613q-4.46 8.606-7.251 13.372t-2.389 8.339a10.243 10.243 0 0 0 3.156 6.249 9.235 9.235 0 0 0 15.739-6.483 19 19 0 0 0-2.175-7.976L10.947 1.337"
        data-name="Path 418"
      />
    </g>
  </svg>
);

const Person: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="304.186" height="834.923">
    <g data-name="Group 74">
      <g data-name="Group 17">
        <path
          fill="#f0f0f7"
          d="M260.109 172.385q-10.065-21.585-35.373-27.128-38.8-6.782-47.626-31.795a19.074 19.074 0 0 0 8.971-16.7v-.365q9.409-9.407 11.6-19.616a102.485 102.485 0 0 0 .656-26.253q-3.72-30.045-29.393-45.942-1.677-1.021-3.5-2.042a2.851 2.851 0 0 1-.583-.219.647.647 0 0 1-.292-.073h-14.081a22 22 0 0 0-3.793 1.75q-4.376-2.261-7.95-1.458a43.209 43.209 0 0 0-7.585 2.042q-24.141 8.97-25.819 45.942a156.148 156.148 0 0 0 1.167 26.253q2.188 10.209 11.6 19.616v.365a19.074 19.074 0 0 0 8.971 16.7q-8.825 25.013-47.626 31.795a56.647 56.647 0 0 0-15.1 5.469q-27.059 14.513-26.986 57.538a481.45 481.45 0 0 0 0 86.2 96.121 96.121 0 0 0-12.691 26.034q-9.919 30.406-7.293 76.346a322.894 322.894 0 0 1-16.046 50.76q-2.553 11.887 14 34.639 2.48 1.9 3.793-.948 3.282 3.865 5.543 3.938 1.75 0 2.917-2.334l5.908 4.3q3.136-3.646 0-9.334-8.023-18.668 0-29.242.8 18.523 10.648 18.6v-14.446q2.7-20.2-5.543-31.576-2.48-11.449 15.462-43.463a86.616 86.616 0 0 0 10.284-20.2q9.263-25.6 7.731-63.371 1.313-11.012 9.846-39.014 9.846 109.531.729 131.117-11.082 30.482-13.925 80.144-3.063 53.38 3.355 128.856-23.7 52.068.583 127.4 11.815 52.794-12.618 82.834-4.157 5.4-4.376 10.064a10.323 10.323 0 0 0 .656 4.375q1.6 4.375 7.148 8.095a19.612 19.612 0 0 1 13.931 2.188q14.66 7.365 22.756 0 3.209-3.719 3.428-10.282a33.995 33.995 0 0 0-.146-4.375 67.962 67.962 0 0 0-1.9-9.48l.146-.51q11.159-12.178 4.887-25.232l-3.938-15.97q-2.261-8.824 9.336-57.318 11.6-27.93 6.418-106.1 10.138-33.91 17.65-70.08 7-33.982 15.025-64.465.511-2.042 1.021-4.011-6.126 0-10.5-6.2a23.931 23.931 0 0 1-4.23-13.272 23.931 23.931 0 0 0 4.228 13.273q4.376 6.2 10.5 6.2t10.43-6.2a24.825 24.825 0 0 0 4.376-13.272 24.825 24.825 0 0 1-4.373 13.272q-4.3 6.2-10.43 6.2.511 1.969 1.094 4.011 7.95 30.555 14.952 64.465 7.512 36.17 17.65 70.08-5.178 78.174 6.418 106.1 11.6 48.494 9.336 57.318l-3.938 15.97q-6.272 13.053 4.887 25.232l.146.51a60.77 60.77 0 0 0-1.823 9.48 34 34 0 0 0-.146 4.375q.146 6.563 3.355 10.282 8.1 7.365 22.756 0a19.612 19.612 0 0 1 13.931-2.188q5.543-3.719 7.22-8.095a10.322 10.322 0 0 0 .656-4.375q-.292-4.667-4.449-10.064-24.433-30.045-12.618-82.841 24.287-75.33.583-127.4 6.418-75.476 3.355-128.856-2.844-49.661-13.93-80.143-9.117-21.585 3.5-131.117 5.762 28 7.075 39.014-2.188 54.547 18.015 83.571 6.2 11.084 9.992 19.762 7.075 16.189 5.47 23.7a31.955 31.955 0 0 0-5.47 13.418 57.911 57.911 0 0 0-.073 18.158v14.439q9.846-.073 10.648-18.6 8.023 10.574 0 29.242-3.136 5.688 0 9.334l5.908-4.3q2.553 5.251 8.46-1.6 1.313 2.844 3.793.948 16.556-22.752 14-34.639A322.9 322.9 0 0 1 286.8 396.84q3.938-68.33-19.984-102.385a481.454 481.454 0 0 0 0-86.2q0-21.512-6.71-35.878m-96.489-27.703a134.783 134.783 0 0 1 28.444-4.813 134.783 134.783 0 0 0-28.444 4.813m-52.148-4.74a99.261 99.261 0 0 1 28.153 4.886 99.261 99.261 0 0 0-28.153-4.886m-1.97 98.37a2.077 2.077 0 0 1-1.6.729 2.306 2.306 0 0 1-1.678-.729 2.182 2.182 0 0 1-.656-1.6 2.247 2.247 0 0 1 2.334-2.334 2.183 2.183 0 0 1 1.6.656 2.305 2.305 0 0 1 .729 1.677 2.077 2.077 0 0 1-.729 1.6m90.731.729a2.51 2.51 0 0 1-2.334-2.334 2.305 2.305 0 0 1 .729-1.677 2.183 2.183 0 0 1 1.6-.656 2.247 2.247 0 0 1 2.334 2.334 2.182 2.182 0 0 1-.656 1.6 2.306 2.306 0 0 1-1.677.729m-115.962 3.437q7.075 9.918 56.962 2.188-49.887 7.73-56.962-2.188m70.09 140.086a3.046 3.046 0 0 1-2.407 1.094 3.42 3.42 0 0 1-2.48-1.094 3.141 3.141 0 0 1-1.021-2.406 3.486 3.486 0 0 1 3.5-3.5 3.142 3.142 0 0 1 2.407 1.021 3.419 3.419 0 0 1 1.094 2.479 3.045 3.045 0 0 1-1.094 2.406m-108.6-85.029q9.773-.8 13.639 5.688-3.866-6.49-13.639-5.688m214.209-.438q-11.524-.219-17.5 5.688 5.981-5.907 17.5-5.688m-36.1-54.62q-7.075 9.918-56.962 2.188 49.886 7.73 56.96-2.187Z"
          data-name="Path 368"
        />
        <path
          fill="#7f939c"
          d="M151.616 384.368a4.174 4.174 0 0 0 3.881-3.881 3.792 3.792 0 0 0-1.213-2.749 3.483 3.483 0 0 0-2.668-1.132 3.865 3.865 0 0 0-3.881 3.881 3.483 3.483 0 0 0 1.132 2.668 3.792 3.792 0 0 0 2.749 1.213m51.752-151.159a2.3 2.3 0 0 0 1.779.809 2.556 2.556 0 0 0 1.86-.809 2.42 2.42 0 0 0 .728-1.779 2.491 2.491 0 0 0-2.588-2.588 2.42 2.42 0 0 0-1.779.728 2.557 2.557 0 0 0-.809 1.86 2.3 2.3 0 0 0 .809 1.779m-100.593.809a2.783 2.783 0 0 0 2.588-2.588 2.557 2.557 0 0 0-.809-1.86 2.42 2.42 0 0 0-1.779-.728 2.491 2.491 0 0 0-2.588 2.588 2.42 2.42 0 0 0 .728 1.779 2.557 2.557 0 0 0 1.86.808Z"
          data-name="Path 369"
        />
      </g>
      <path
        fill="none"
        stroke="#7f939c"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M152.093 462.348q.511 1.969 1.094 4.011 7.95 30.56 14.952 64.474 7.512 36.176 17.65 70.09-5.178 78.186 6.418 106.12 11.6 48.5 9.336 57.327l-3.938 15.973q-6.272 13.055 4.887 25.235l.146.511a60.784 60.784 0 0 0-1.823 9.481 34.012 34.012 0 0 0-.146 4.376q.146 6.564 3.355 10.284 8.1 7.366 22.756 0a19.609 19.609 0 0 1 13.931-2.188q5.543-3.72 7.22-8.1a10.325 10.325 0 0 0 .656-4.376q-.292-4.668-4.449-10.065-24.433-30.049-12.618-82.854 24.287-75.341.583-127.417 6.418-75.487 3.355-128.875-2.844-49.668-13.93-80.155-9.117-21.589 3.5-131.136 5.762 28.007 7.075 39.02-2.188 54.555 18.015 83.583 6.2 11.086 9.992 19.765 7.075 16.191 5.47 23.7a31.962 31.962 0 0 0-5.47 13.42 57.928 57.928 0 0 0-.073 18.161v14.441q9.846-.073 10.648-18.6 8.023 10.576 0 29.247-3.136 5.689 0 9.336l5.908-4.3q2.553 5.251 8.46-1.6 1.313 2.845 3.793.948 16.556-22.756 14-34.644a322.978 322.978 0 0 1-16.046-50.762q3.938-68.34-19.984-102.4a481.6 481.6 0 0 0 0-86.209q0-21.516-6.71-35.884-10.065-21.589-35.373-27.132-38.8-6.783-47.626-31.8a19.078 19.078 0 0 0 8.971-16.7v-.365q9.409-9.409 11.6-19.619a102.515 102.515 0 0 0 .656-26.256q-3.72-30.049-29.393-45.949-1.677-1.021-3.5-2.042a2.851 2.851 0 0 1-.583-.219.647.647 0 0 1-.292-.073m-14.076 0a22 22 0 0 0-3.793 1.75q-4.376-2.261-7.95-1.459a43.2 43.2 0 0 0-7.585 2.042q-24.141 8.971-25.819 45.949a156.193 156.193 0 0 0 1.167 26.256q2.188 10.211 11.6 19.619v.365a19.078 19.078 0 0 0 8.971 16.7q-8.825 25.017-47.626 31.8a56.642 56.642 0 0 0-15.1 5.47q-27.059 14.514-26.986 57.545a481.592 481.592 0 0 0 0 86.209 96.14 96.14 0 0 0-12.691 26.038q-9.919 30.414-7.293 76.362a322.977 322.977 0 0 1-16.046 50.762q-2.553 11.888 14 34.644 2.48 1.9 3.793-.948 3.282 3.865 5.543 3.938 1.75 0 2.917-2.334l5.908 4.3q3.136-3.647 0-9.336-8.023-18.671 0-29.247.8 18.525 10.648 18.6v-14.435q2.7-20.2-5.543-31.581-2.48-11.451 15.462-43.469a86.633 86.633 0 0 0 10.284-20.2q9.263-25.6 7.731-63.38 1.313-11.013 9.846-39.02 9.846 109.548.729 131.136-11.084 30.484-13.927 80.153-3.063 53.388 3.355 128.875-23.7 52.075.583 127.417 11.815 52.8-12.618 82.854-4.157 5.4-4.376 10.065a10.326 10.326 0 0 0 .656 4.376q1.6 4.376 7.148 8.1a19.609 19.609 0 0 1 13.93 2.179q14.66 7.366 22.756 0 3.209-3.72 3.428-10.284a34.005 34.005 0 0 0-.146-4.376 67.978 67.978 0 0 0-1.9-9.481l.146-.511q11.159-12.18 4.887-25.235l-3.938-15.973q-2.261-8.825 9.336-57.327 11.6-27.934 6.418-106.12 10.138-33.915 17.65-70.09 7-33.987 15.025-64.474.511-2.042 1.021-4.011-6.126 0-10.5-6.2a23.937 23.937 0 0 1-4.23-13.274m27.2-440.743a21.559 21.559 0 0 0-13.785 0m16.119 440.743a24.831 24.831 0 0 1-4.376 13.274q-4.3 6.2-10.43 6.2"
        data-name="Path 370"
      />
      <path
        fill="none"
        stroke="#7f939c"
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M163.22 141.415a112.613 112.613 0 0 1 27.174-5.337m-76.994.081a83.1 83.1 0 0 1 26.9 5.418M87.41 249.852q6.759 11 54.419 2.426M50.62 310.903q9.337-.89 13.03 6.307m191.615-6.792q-11.009-.243-16.723 6.307m-17.772-66.873q-6.759 11-54.419 2.426"
        data-name="Path 371"
      />
    </g>
  </svg>
);

const Flip: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="45.69" height="23.859">
    <g fill="#7f939c" data-name="Group 35">
      <g data-name="Group 33">
        <path d="m26.612 5.964 8.259-5.965v11.93Z" data-name="Polygon 1" />
        <path
          d="M34.6 3.992a21.542 21.542 0 0 1 7.941 2.713 6.074 6.074 0 0 1 3.142 5.485c-.334 6.9-11.083 9.117-11.083 9.117s7.612-6.064 7.361-9.117S34.6 8.551 34.6 8.551Z"
          data-name="Path 376"
        />
      </g>
      <g data-name="Group 34">
        <path d="m19.078 17.895-8.259 5.965V11.93Z" data-name="Polygon 1" />
        <path
          d="M11.09 19.867a21.542 21.542 0 0 1-7.941-2.712 6.074 6.074 0 0 1-3.142-5.488c.335-6.9 11.083-9.114 11.083-9.114s-7.612 6.064-7.361 9.114 7.361 3.641 7.361 3.641Z"
          data-name="Path 376"
        />
      </g>
    </g>
  </svg>
);

const Tag: FC<{ tag: string; checked: boolean; onChange: (checked: boolean) => void; first?: boolean }> = ({
  tag,
  checked,
  onChange,
  first,
}) => (
  <AntdTag.CheckableTag
    checked={checked}
    onChange={onChange}
    style={{
      padding: '10px 20px',
      display: 'flex',
      alignItems: 'center',
      height: '45px',
      background: checked ? 'gray' : 'white',
      marginRight: first ? '0' : undefined,
      font: 'normal normal 600 18px/13px Source Sans Pro',
      color: '#4D565C',
    }}
  >
    {tag}
  </AntdTag.CheckableTag>
);
const Divider: FC = () => <AntdDivider type="vertical" orientation={'center'} style={{ backgroundColor: '#A4AFB7' }} />;

const columns = [
  { title: 'שעה', dataIndex: 'at' },
  { title: 'פרוצדורה', dataIndex: 'procedure' },
  { title: 'בוצע ע״י', dataIndex: 'performer' },
  { title: 'הערות', dataIndex: 'notes' },
];

export const InfoPanel2: FC = () => {
  const [tags, setTags] = useState<Record<string, boolean>>({});
  const onTagChange = useCallback(
    (value: string) => (checked: boolean) => setTags((v) => ({ ...v, [value]: checked })),
    [],
  );
  return (
    <div style={{ width: '100vw', height: '100vh', display: 'flex' }}>
      <div
        style={{
          width: '715px',
          height: '1200px',
          background: '#F0F0F7 0% 0% no-repeat padding-box',
          display: 'flex',
          flexDirection: 'column',
          paddingRight: '56px',
          paddingTop: '57px',
        }}
      >
        <div style={{ width: '100%', display: 'inline-flex' }}>
          <span
            style={{
              font: 'normal normal 600 28px/37px Segoe UI',
              color: '#605F86',
            }}
          >
            אלמוני/ת
          </span>
        </div>
        <div style={{ width: '100%', display: 'inline-flex', alignItems: 'center' }}>
          <span style={{ font: 'normal normal normal 20px/27px Segoe UI', color: '#605F86', marginLeft: '51px' }}>
            ת.ז
          </span>
          <InputNumber controls={false} size={'small'} style={{ width: '164px' }} />
          <Radio.Group defaultValue={'adult'} style={{ marginRight: '62px' }}>
            <Radio value="adult">בוגר</Radio>
            <Radio value="child">ילד</Radio>
            <Radio value="infant">תינוק</Radio>
          </Radio.Group>
        </div>
        <div
          style={{
            width: '100%',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginTop: '10px',
          }}
        >
          <div>
            <span
              style={{
                font: 'normal normal normal 20px/27px Segoe UI',
                color: '#605F86',
                marginLeft: '10px',
              }}
            >
              מס׳ ידון
            </span>
            <InputNumber controls={false} size={'small'} style={{ width: '164px' }} />
          </div>
          <div>
            <Button style={{ marginLeft: '35px' }} type={'primary'}>
              הבא נתונים
            </Button>
          </div>
        </div>
        <div
          style={{
            width: '100%',
            display: 'inline-flex',
            alignItems: 'center',
            marginTop: '20px',
          }}
        >
          <Tag tag={'חוסר הכרה'} checked={tags['חוסר הכרה']} onChange={onTagChange('חוסר הכרה')} first />
          <Tag tag={'תגובת קרב'} checked={tags['תגובת קרב']} onChange={onTagChange('תגובת קרב')} />
          <Tag tag={'שאיפת עשן'} checked={tags['שאיפת עשן']} onChange={onTagChange('שאיפת עשן')} />
          <Tag tag={'מעיכה'} checked={tags['מעיכה']} onChange={onTagChange('מעיכה')} />
        </div>
        <div
          style={{
            width: '100%',
            display: 'inline-flex',
            alignItems: 'center',
            marginTop: '10px',
          }}
        >
          <Tag tag={'הדף'} checked={tags['הדף']} onChange={onTagChange('הדף')} first />
          <Tag tag={'ירי'} checked={tags['ירי']} onChange={onTagChange('ירי')} />
          <Tag tag={'קינמטיקה'} checked={tags['קינמטיקה']} onChange={onTagChange('קינמטיקה')} />
        </div>
        <div>
          <Menu
            style={{ backgroundColor: 'unset', marginRight: '-20px', marginTop: '20px' }}
            defaultActiveFirst
            mode={'horizontal'}
            items={[
              {
                label: 'פרוצדורות ותרופות',
                key: 'procedures',
              },
              {
                label: 'הערות',
                key: 'notes',
              },
            ]}
          />
          <div
            style={{
              marginTop: '15px',
              marginRight: '-20px',
              font: 'normal normal 600 22px/30px Segoe UI',
              color: '#6462A3',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <Button type={'text'} icon={<Procedures />} style={{ display: 'flex', alignItems: 'center' }}>
              פרוצדורות
            </Button>
            <Divider />
            <Button type={'text'} icon={<Drugs />} style={{ display: 'flex', alignItems: 'center' }}>
              תרופות
            </Button>
            <Divider />
            <Button type={'text'} icon={<Vitals />} style={{ display: 'flex', alignItems: 'center' }}>
              מדדים
            </Button>
            <Divider />
            <Button type={'text'} icon={<Other />} style={{ display: 'flex', alignItems: 'center' }}>
              אחר
            </Button>
          </div>
        </div>
        <div style={{ width: '100%', marginTop: '30px' }}>
          <Table columns={columns} locale={{ emptyText: 'טרם נרשמו טיפולים' }} size={'small'} />
        </div>
      </div>
      <div style={{ display: 'grid', width: '1205px', height: '1200px', background: 'white' }}>
        <div
          style={{
            marginLeft: '10px',
            marginTop: '10px',
            position: 'relative',
            top: 0,
            left: 0,
            display: 'flex',
            justifySelf: 'end',
            alignItems: 'baseline',
          }}
        >
          <span>
            <Moment format={'hh:mm'} style={{ marginRight: '5px' }} />
            <Moment format={'A'} />
          </span>
          <Button type={'primary'} style={{ marginRight: '10px' }}>
            המשך טיפול
          </Button>
        </div>
        <div
          style={{
            marginLeft: '10px',
            position: 'relative',
            top: '50%',
            left: 0,
            display: 'flex',
            justifySelf: 'end',
            flexDirection: 'column',
          }}
        >
          טרם נלקחו מדדים
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', direction: 'ltr' }}>
            <Card style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
              <div>None</div>
              <div>דופק</div>
              <div>Pulse</div>
            </Card>
            <Card style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
              <div>None</div>
              <div>לחץ דם</div>
              <div>B.P.</div>
            </Card>
            <Card style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
              <div>None</div>
              <div>חום</div>
              <div>Temperature</div>
            </Card>
            <Card style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
              <div>None</div>
              <div>סטורציה</div>
              <div>Saturation</div>
            </Card>
            <Card style={{ margin: '6px', display: 'flex', flexDirection: 'column' }}>
              <div>0%</div>
              <div>כוויות</div>
              <div>Burns</div>
            </Card>
          </div>
        </div>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            marginTop: '-550px',
            marginRight: '-200px',
          }}
        >
          <div style={{ marginBottom: '10px' }}>
            <Flip />
          </div>
          <div style={{ display: 'flex', justifyContent: 'start' }}>
            <span style={{ marginTop: '25px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
              L
            </span>
            <Person />
            <span style={{ marginTop: '25px', font: 'normal normal normal 40px/53px Segoe UI', color: '#7F939C' }}>
              R
            </span>
          </div>
          <div style={{ marginTop: '20px' }}>
            <Radio.Group defaultValue={'injuries'}>
              <Radio value="injuries" style={{ marginLeft: '50px' }}>
                פציעות
              </Radio>
              <Radio value="burns">כוויות</Radio>
            </Radio.Group>
          </div>
        </div>
      </div>
    </div>
  );
};
