<%inherit file="base.mako"></%inherit>

<%block name="content">
% for i,user in enumerate(users):
    <div>${user.name}</div>
% end for
</%block>
