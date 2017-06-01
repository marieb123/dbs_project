--DROP TABLE contains;
--DROP TABLE hashtag_table;
--DROP TABLE tweet;

CREATE TABLE 
tweet (
    tweet_id integer PRIMARY KEY,
    handle text NOT NULL,
    text text NOT NULL,
    is_retweet boolean NOT NULL,
    original_author text,
    date timestamp without time zone NOT NULL,
    is_quote_status boolean NOT NULL,
    retweet_count integer NOT NULL,
    favorite_count integer NOT NULL,
    
    --is_retweet=True if and only if original_author not null
    CONSTRAINT original_tweet_author CHECK 
        (CASE WHEN is_retweet THEN original_author<>'' ELSE original_author='' END
        AND CASE WHEN original_author='' THEN NOT is_retweet ELSE is_retweet END)
    );
                                                
CREATE TABLE hashtag_table (
    hashtag text PRIMARY KEY,
    --first character of hashtag is #
    CHECK (substring(hashtag, 1,1)='#')
    );
    
CREATE TABLE contains (
    tweet_id integer REFERENCES tweet (tweet_id),
    hashtag text REFERENCES hashtag_tableac (hashtag)
    )