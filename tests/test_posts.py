def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1

def test_post_page_renders_template_and_context(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )

        response = client.get('/posts/0')
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == posts_list[0]['title']
        assert context['post'] == posts_list[0]

def test_post_page_contains_all_post_data(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/0')
    text = response.text
    assert posts_list[0]['title'] in text
    assert posts_list[0]['author'] in text
    assert '10.03.2025' in text
    assert posts_list[0]['text'] in text
    assert posts_list[0]['image_id'] in text

def test_post_page_has_comment_form(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/0')
    text = response.text
    assert 'Оставьте комментарий' in text
    assert '<form' in text and 'textarea' in text and 'type="submit"' in text

def test_post_404_for_invalid_index_negative(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/-1')
    assert response.status_code == 404

def test_post_404_for_invalid_index_out_of_range(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/5')
    assert response.status_code == 404

def test_posts_page_lists_cards_and_links(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts')
    text = response.text
    assert 'Последние посты' in text
    assert 'Читать дальше' in text

def test_posts_template_date_format(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts')
    assert '10.03.2025' in response.text

def test_index_template_used(client, captured_templates):
    with captured_templates as templates:
        _ = client.get('/')
        assert len(templates) == 1
        template, _ = templates[0]
        assert template.name == 'index.html'

def test_about_template_used(client, captured_templates):
    with captured_templates as templates:
        _ = client.get('/about')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'about.html'
        assert context['title'] == 'Об авторе'

def test_base_template_inheritance_posts(client):
    response = client.get('/posts')
    assert '<nav class="navbar navbar-expand-lg navbar-dark bg-dark">' in response.text

def test_footer_present_on_all_pages(client):
    for path in ['/', '/posts', '/about']:
        response = client.get(path)
        assert 'ФИО:' in response.text and 'Группа:' in response.text

def test_post_template_includes_image_tag(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/0')
    assert '<img' in response.text

def test_comments_section_present(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list, autospec=True)
    response = client.get('/posts/0')
    assert 'Комментарии' in response.text

def test_posts_context_contains_posts_key(client, captured_templates):
    with captured_templates as templates:
        _ = client.get('/posts')
        _, context = templates[0]
        assert 'posts' in context
