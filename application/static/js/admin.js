var app = {};

/**
 * Represents a single blogpost and its contents.
 */
app.BlogPost = Backbone.Model.extend({
    defaults: {
        title: '',
        date_published: null,
        content: '',
        draft: true
    },

    urlRoot: '/api/blog',
    isDraft: function() {
        return this.draft;
    },
    parse: function (response) {
        // This hack is needed because sometimes we are accessing a single blogpost and that is
        // wrapped in a data tag, and other times we are accessing a collection of blogposts,
        // in which case the unwrapping is already handled in BlogList.
        if (response['data'] != undefined) {
            return response['data'];
        }
        return response;
    }
});

// Container for blogposts.
app.BlogList = Backbone.Collection.extend({
    model: app.BlogPost,
    url: '/api/blog',
    // Remove the data wrapper that jsonify requires.
    parse: function(response) {
        return response['data']
    }
});

/**
 * Table based view with summary information about blog posts.
 */
app.BlogListViewItem = Backbone.View.extend({
    tagName: 'tr',
    template: _.template($("#blogOverviewTemplate").html()),

    events: {
        'click .edit': 'edit',
        'click .delete': 'del'
    },

    edit: function() {
      app.router.navigate("blog/" + this.model.id, true);
    },

    del: function() {
        this.model.destroy();
    },

    render: function() {
        this.$el.empty();
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },

    initialize: function() {
        this.model.on('change', this.render, this);
        this.model.on('delete', this.remove, this);
    }
});

/**
 * Editing a specific blog post.
 */
app.BlogDetailView = Backbone.View.extend({
    el: "#adminContainer",

    events: {
        'click .save': 'save'
    },

    save: function() {
        this.model.set({title: this.$("#postTitle").val(),
            content: this.simpleMde.value(),
            draft: this.$("#draft")[0].checked });
        this.model.save();
    },

    initialize: function(id) {
        console.log(id);
        var parent = this;
        var tmpModel = new app.BlogPost({id: id});
        tmpModel.fetch({
            success: function(model, response) {
                parent.model = model;
                parent.render();
            }
        });
    },

    template: _.template($("#blogEditViewTemplate").html()),

    render: function() {
        var draft = this.model.draft ? "checked" : "";
        var tmpl_data = _.extend(this.model.toJSON(), draft);
        this.$el.html(this.template(tmpl_data));
        // Initialize the markdown editor.
        this.simpleMde = new SimpleMDE( { element: $("#postContent")[0] });
        this.simpleMde.render();
        return this;
    }
});

// Main application view
app.BlogListView = Backbone.View.extend({
    el: "#adminContainer",

    initialize: function() {
        console.log("Init");
        app.blogList.on('add', this.addAll, this);
        app.blogList.on('reset', this.addAll, this);
        app.blogList.fetch();
        // Draw the table on the page.
        this.render();
    },
    addOne: function(post) {
        console.log(post.toJSON());
        var view = new app.BlogListViewItem({model: post});
        $("#blogPostList").append(view.render().el);
    },
    addAll: function() {
        console.log("Adding all");
        app.blogList.each(this.addOne, this);
    },
    render: function() {
        this.$el.empty();
        this.$el.html($("#blogPostContainerTemplate").html());
        return this;
    }
});

app.Router = Backbone.Router.extend({
    routes: {
        'blog': 'blog',
        'blog/:id': 'blogEdit'
    },
    blog: function() {
        app.blogListView = new app.BlogListView();
    },
    blogEdit: function(id) {
        app.blogDetailView = new app.BlogDetailView(id);
    }
});

$(document).ready(function() {
    app.blogList = new app.BlogList();
    app.router = new app.Router();
    Backbone.history.start();
});
