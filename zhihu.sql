create table zhihu_car
(
    answer_num       int auto_increment
        primary key,
    question_num     int          null,
    question_title   text         null,
    is_full_video    text         null,
    answer_text      longtext     null,
    img_num          int          null,
    href_num         int          null,
    agree_num        int          null,
    comment_num      int          null,
    reward_num       int          null,
    is_invite        text         null,
    is_profess       text         null,
    is_collect       text         null,
    first_post_time  datetime     null,
    last_revise_time datetime     null,
    positive_prob    varchar(255) null,
    sentiment        int          null
);


