/*
 * Messages.java: common vote-counting messages
 * Copyright (C) 2014 Shardul C.
 *
 * This file is part of VoteCounter.
 *
 * VoteCounter is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 *
 * VoteCounter is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * VoteCounter. If not, see <http://www.gnu.org/licenses/>.
 *
 * Bugs, tips, suggestions, requests to <shardul.chiplunkar@gmail.com>
 * or <mjuvekar7@gmail.com>.
 */
package messages;

/**
 * Common messages sent between the client and the server.
 *
 * The string value of each item is only actually used for the {@code PORT}
 * item.
 *
 * @author Shardul C.
 */
public enum Messages {
    GET_GROUP ("get_group"),
    VOTE ("vote"),
    GOODBYE ("goodbye"),
    // not a message but used anyway
    PORT ("13875");

    public String msg;
    private Messages(String msg) {
        this.msg = msg;
    }

    @Override
    public String toString() {
        return this.msg;
    }
}
